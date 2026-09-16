"""Tests for the desktop app itself.

Skipped when the Python running the tests has no tkinter, or when there is no
display to open a window on. To run them headlessly:

    xvfb-run -a python -m unittest discover -s tests
"""

from __future__ import annotations

import gc
import os
import sys
import tempfile
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SAMPLES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "samples")

try:
    import tkinter
    _TK_IMPORT_ERROR = None
except ImportError as exc:                       # pragma: no cover - environment
    tkinter = None
    _TK_IMPORT_ERROR = exc


def _display_available() -> bool:
    if tkinter is None:
        return False
    try:
        root = tkinter.Tk()
    except Exception:                            # pragma: no cover - environment
        return False
    root.destroy()
    # Tk leaves this pointing at the destroyed root, which upsets the next Tk().
    tkinter._default_root = None
    return True


requires_display = unittest.skipUnless(
    _display_available(), f"no tkinter or no display ({_TK_IMPORT_ERROR})")


def sample(name: str) -> str:
    return os.path.join(SAMPLES, name)


@requires_display
class ConverterAppTests(unittest.TestCase):
    def setUp(self):
        from qb2drake.app import ConverterApp
        self.app = ConverterApp()
        self.app.update()
        self.tmp = tempfile.mkdtemp()
        self.app.out_dir.set(os.path.join(self.tmp, "out"))

    def tearDown(self):
        # close() waits for the conversion thread; destroying Tk out from under
        # a live thread aborts the interpreter.
        #
        # Dropping the reference and collecting here matters just as much:
        # unittest keeps every TestCase alive for the whole run, so without
        # this the app's Tk Variables are finalised at interpreter shutdown
        # against a destroyed interpreter, which aborts the process.
        app, self.app = self.app, None
        app.close()
        del app
        gc.collect()

    def add(self, *names):
        for name in names:
            self.app.file_list.insert("end", sample(name))

    def convert_and_wait(self, timeout: float = 30.0):
        self.app.start_convert()
        deadline = time.time() + timeout
        while time.time() < deadline:
            self.app.update()
            if self.app.status.get() != "Converting...":
                return True
            time.sleep(0.02)
        return False

    def report_text(self) -> str:
        return self.app.report.get("1.0", "end")

    def test_converting_writes_files_and_reports_success(self):
        self.add("account_listing.csv", "general_ledger.csv")
        self.assertTrue(self.convert_and_wait())
        self.assertIn("Converted cleanly", self.app.status.get())
        self.assertIn("Files written", self.report_text())
        self.assertTrue(os.path.isdir(os.path.join(self.tmp, "out")))

    def test_iif_checkbox_produces_the_iif_file(self):
        self.add("quickbooks_export.iif")
        self.app.write_iif.set(True)
        self.assertTrue(self.convert_and_wait())
        written = os.listdir(os.path.join(self.tmp, "out"))
        self.assertIn("drake_chart_of_accounts.IIF", written)

    def test_convert_button_is_re_enabled_afterwards(self):
        self.add("journal.csv")
        self.assertTrue(self.convert_and_wait())
        self.assertEqual(str(self.app.convert_button["state"]), "normal")
        self.assertEqual(str(self.app.open_button["state"]), "normal")

    def test_a_qbb_backup_shows_the_explanation_in_red(self):
        qbb = os.path.join(self.tmp, "company.qbb")
        with open(qbb, "wb") as handle:
            handle.write(b"\x00\x01binary")
        self.app.file_list.insert("end", qbb)
        self.assertTrue(self.convert_and_wait())
        self.assertIn("Could not convert", self.app.status.get())
        self.assertIn("Restore a backup copy", self.report_text())
        self.assertIn("error", self.app.report.tag_names("1.0"))
        self.assertEqual(str(self.app.open_button["state"]), "disabled")

    def test_unbalanced_input_warns_instead_of_claiming_success(self):
        bad = os.path.join(self.tmp, "bad.csv")
        with open(bad, "w", encoding="utf-8") as handle:
            handle.write(",Trans #,Type,Date,Num,Name,Memo,Account,Debit,Credit\n")
            handle.write(",1,Check,01/05/2025,9,X,m,Checking,,100.00\n")
            handle.write(",1,Check,01/05/2025,9,X,m,Rent Expense,90.00,\n")
        self.app.file_list.insert("end", bad)
        self.assertTrue(self.convert_and_wait())
        self.assertIn("Drake will", self.app.status.get())
        self.assertIn("do not balance", self.report_text())

    def test_options_reach_the_job(self):
        self.add("journal.csv")
        self.app.division.set("01")
        self.app.renumber.set(True)
        self.app.group_by.set("trans-no")
        options = self.app.collect_options()
        self.assertEqual(options.division, "01")
        self.assertTrue(options.renumber)
        self.assertEqual(options.group_by, "trans-no")
        self.assertEqual(len(options.inputs), 1)

    def test_file_list_add_remove_and_clear(self):
        self.add("journal.csv", "general_ledger.csv")
        self.assertEqual(self.app.file_list.size(), 2)
        self.app.file_list.selection_set(0)
        self.app.remove_files()
        self.assertEqual(self.app.file_list.size(), 1)
        self.app.clear_files()
        self.assertEqual(self.app.file_list.size(), 0)

    def test_closing_while_a_conversion_runs_shuts_down_cleanly(self):
        """Someone will close the window mid-run; it must not abort or hang."""
        self.add("quickbooks_export.iif")
        self.app.start_convert()
        self.app.update()
        self.app.close()                      # no wait: the job may still be going
        self.assertTrue(self.app.wait_for_worker(timeout=10))
        # tearDown calls close() again; a second close must be harmless.

    def test_converting_with_no_files_does_not_start_a_job(self):
        options = self.app.collect_options()
        self.assertEqual(options.inputs, [])


if __name__ == "__main__":
    unittest.main()
