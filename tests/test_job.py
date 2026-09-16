"""Tests for the headless conversion job the desktop app runs."""

from __future__ import annotations

import csv
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qb2drake.job import JobOptions, describe_result, run_job

SAMPLES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "samples")


def sample(name: str) -> str:
    return os.path.join(SAMPLES, name)


class JobValidationTests(unittest.TestCase):
    def test_no_input_is_a_plain_english_error(self):
        result = run_job(JobOptions(inputs=[], out_dir="out"))
        self.assertFalse(result.ok)
        self.assertIn("at least one QuickBooks export", result.error)

    def test_no_output_folder_is_a_plain_english_error(self):
        result = run_job(JobOptions(inputs=[sample("journal.csv")], out_dir=""))
        self.assertFalse(result.ok)
        self.assertIn("folder", result.error)

    def test_a_qbb_backup_explains_itself_rather_than_crashing(self):
        with tempfile.TemporaryDirectory() as tmp:
            qbb = os.path.join(tmp, "company.qbb")
            with open(qbb, "wb") as handle:
                handle.write(b"\x00\x01binary")
            result = run_job(JobOptions(inputs=[qbb], out_dir=tmp))
        self.assertFalse(result.ok)
        self.assertIn("Restore a backup copy", result.error)
        self.assertEqual(describe_result(result), result.error)


class JobRunTests(unittest.TestCase):
    def run_job(self, names, **kwargs):
        tmp = tempfile.mkdtemp()
        options = JobOptions(inputs=[sample(n) for n in names], out_dir=tmp, **kwargs)
        return run_job(options), tmp

    def test_clean_run_writes_both_files(self):
        result, tmp = self.run_job(["quickbooks_export.iif"])
        self.assertTrue(result.ok)
        self.assertTrue(result.clean)
        self.assertEqual(len(result.files), 2)
        for _, path in result.files:
            self.assertTrue(os.path.exists(path), path)

    def test_iif_option_adds_a_third_file_with_the_right_extension(self):
        result, _ = self.run_job(["quickbooks_export.iif"], write_iif=True)
        labels = dict((label, path) for label, path in result.files)
        self.assertIn("Chart of Accounts (IIF)", labels)
        self.assertTrue(labels["Chart of Accounts (IIF)"].endswith(".IIF"))

    def test_problems_are_counted_but_the_run_still_succeeds(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = os.path.join(tmp, "bad.csv")
            with open(bad, "w", newline="", encoding="utf-8") as handle:
                writer = csv.writer(handle)
                writer.writerow(["", "Trans #", "Type", "Date", "Num", "Name",
                                 "Memo", "Account", "Debit", "Credit"])
                writer.writerow(["", "1", "Check", "01/05/2025", "9", "X", "m",
                                 "Checking", "", "100.00"])
                writer.writerow(["", "1", "Check", "01/05/2025", "9", "X", "m",
                                 "Rent Expense", "90.00", ""])
            result = run_job(JobOptions(inputs=[bad], out_dir=os.path.join(tmp, "o")))
        self.assertTrue(result.ok)          # files were still written
        self.assertFalse(result.clean)      # but Drake would reject them
        self.assertGreater(result.error_count, 0)

    def test_templates_drive_the_output_header_and_filenames(self):
        with tempfile.TemporaryDirectory() as tmp:
            header = ["Division", "Account Number", "Date", "Journal",
                      "Reference", "Description", "Debit", "Credit", "Batch ID"]
            template = os.path.join(tmp, "Blank_JournalEntries_Template.csv")
            with open(template, "w", newline="", encoding="utf-8") as handle:
                csv.writer(handle).writerow(header)

            result = run_job(JobOptions(
                inputs=[sample("journal.csv")],
                out_dir=os.path.join(tmp, "out"),
                templates=[template]))

            self.assertTrue(result.ok)
            written = dict(result.files)["Journal Entries"]
            self.assertTrue(written.endswith("JournalEntries.csv"))
            with open(written, newline="", encoding="utf-8") as handle:
                self.assertEqual(next(csv.reader(handle)), header)
            self.assertEqual(result.unmatched_columns[template], ["Batch ID"])


class DescribeResultTests(unittest.TestCase):
    def test_next_steps_cover_both_import_doors_and_the_client_code(self):
        tmp = tempfile.mkdtemp()
        result = run_job(JobOptions(inputs=[sample("quickbooks_export.iif")],
                                    out_dir=tmp, write_iif=True))
        text = describe_result(result)
        self.assertIn("Tools > Spreadsheets > Import", text)
        self.assertIn("File > Import > Import QuickBooks", text)
        self.assertIn("you choose it", text)
        self.assertIn("8 letters, digits or underscores", text)
        self.assertIn("Files written", text)

    def test_unmatched_columns_are_surfaced_to_the_reader(self):
        with tempfile.TemporaryDirectory() as tmp:
            template = os.path.join(tmp, "Blank_JournalEntries_Template.csv")
            with open(template, "w", newline="", encoding="utf-8") as handle:
                csv.writer(handle).writerow(["Date", "Debit", "Credit", "Widget"])
            result = run_job(JobOptions(inputs=[sample("journal.csv")],
                                        out_dir=os.path.join(tmp, "out"),
                                        templates=[template]))
            self.assertIn("Widget", describe_result(result))


if __name__ == "__main__":
    unittest.main()
