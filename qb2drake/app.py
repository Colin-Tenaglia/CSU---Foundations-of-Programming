"""Desktop front end for the QuickBooks -> Drake Accounting converter.

Laid out in the order the work actually happens: choose the QuickBooks export,
point at Drake's blank templates so the columns line up, pick somewhere to save,
convert, then read what happened. All the accounting logic lives in
qb2drake.job; this module only moves values between widgets and that.

Tkinter is used deliberately -- it ships with Python, so the app runs on a
Windows workstation with nothing else installed.
"""

from __future__ import annotations

import os
import queue
import subprocess
import sys
import threading
import tkinter as tk
from typing import Optional
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText

from .job import JobOptions, JobResult, describe_result, run_job

APP_TITLE = "QuickBooks to Drake Accounting Converter"

QUICKBOOKS_FILETYPES = [
    ("QuickBooks exports", "*.iif *.IIF *.csv *.CSV *.txt *.xlsx *.xls"),
    ("IIF files", "*.iif *.IIF"),
    ("CSV files", "*.csv *.CSV"),
    ("Excel files", "*.xlsx *.xls"),
    ("All files", "*.*"),
]
CSV_FILETYPES = [("CSV files", "*.csv *.CSV"), ("All files", "*.*")]

EXPORT_HELP = """\
Getting the data out of QuickBooks

QuickBooks Desktop
  Best single file -- it carries the accounts and the transactions together:
    File > Utilities > Export > Lists to IIF Files

  Or export two reports and add both here:
    Reports > Accountant & Taxes > General Ledger    (set the date range)
    Reports > Accountant & Taxes > Account Listing
    On each: Excel > Create New Worksheet > Export to a comma separated
    values (.csv) file

  The Account Listing matters. It carries the account types the General
  Ledger leaves out, so adding both gives a properly classified chart.

QuickBooks Online
  Reports > search for Journal, or General Ledger plus Account List
  Set the date range, then Export > Export to Excel or CSV.

A .QBB backup cannot be used
  It is a proprietary backup that only QuickBooks can open. Restore it first
  (File > Open or Restore Company), then export as above.\
"""

IMPORT_HELP = """\
Getting the data into Drake Accounting

Chart of accounts and journal entries
  Tools > Spreadsheets > Import tab
  Choose the type on the left (Chart of Accounts, then Journal Entries),
  browse to the matching file this app wrote, wait for "Properties Detected"
  to fill in, then Check all required fields, then Import.

Why the templates box matters
  Drake's column layout changes between program years. Export the blank
  templates from Tools > Spreadsheets > Export tab and point this app at
  them. The files it writes will then carry Drake's own header row in
  Drake's own order, which is what "Properties Detected" reads.

The .IIF file, if you asked for one
  File > Import > Import QuickBooks
  This wizard imports lists only -- there is no transactions option, which
  is why journal entries go through Spreadsheets instead.

The Client Code
  It is not in your QuickBooks data and there is nothing to look up. It is
  Drake's own identifier for the client and you choose it: up to 8 letters,
  digits or underscores, for example ACME01. A code that does not exist yet
  creates a new client. An existing code imports only what that client is
  missing.

Each selection imports once per client, so check the report before importing.\
"""


def open_in_file_manager(path: str) -> None:
    """Reveal a folder using whatever the platform provides."""
    if sys.platform.startswith("win"):
        os.startfile(path)                                  # noqa: S606
    elif sys.platform == "darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


class TextWindow(tk.Toplevel):
    """A read-only window for the help text."""

    def __init__(self, parent, title: str, body: str):
        super().__init__(parent)
        self.title(title)
        self.transient(parent)
        self.geometry("680x520")
        text = ScrolledText(self, wrap="word", padx=14, pady=12)
        text.pack(fill="both", expand=True)
        text.insert("1.0", body)
        text.configure(state="disabled", font=("TkFixedFont", 10))
        ttk.Button(self, text="Close", command=self.destroy).pack(pady=(0, 10))


class ConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("880x760")
        self.minsize(760, 640)

        self._queue: "queue.Queue[JobResult]" = queue.Queue()
        self._last_out_dir = ""
        self._worker_thread: Optional[threading.Thread] = None
        self._poll_job = None
        self._closed = False

        self.journal_template = tk.StringVar()
        self.chart_template = tk.StringVar()
        self.out_dir = tk.StringVar(value=os.path.join(os.path.expanduser("~"),
                                                       "Drake Import"))
        self.division = tk.StringVar()
        self.write_iif = tk.BooleanVar(value=True)
        self.renumber = tk.BooleanVar(value=False)
        self.group_by = tk.StringVar(value="auto")
        self.status = tk.StringVar(value="Add a QuickBooks export to begin.")

        self._build_menu()
        self._build_body()
        self.protocol("WM_DELETE_WINDOW", self.close)

    # ---------------------------------------------------------------- layout

    def _build_menu(self) -> None:
        menu = tk.Menu(self)
        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Add QuickBooks files...", command=self.add_files)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.destroy)
        menu.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menu, tearoff=0)
        help_menu.add_command(label="Exporting from QuickBooks",
                              command=lambda: TextWindow(self, "Exporting from QuickBooks",
                                                         EXPORT_HELP))
        help_menu.add_command(label="Importing into Drake Accounting",
                              command=lambda: TextWindow(self, "Importing into Drake",
                                                         IMPORT_HELP))
        menu.add_cascade(label="Help", menu=help_menu)
        self.configure(menu=menu)

    def _build_body(self) -> None:
        # Packed before the body: an expanding sibling packed first would
        # leave no room for it.
        ttk.Label(self, textvariable=self.status, relief="sunken",
                  anchor="w", padding=(8, 4)).pack(fill="x", side="bottom")

        outer = ttk.Frame(self, padding=12)
        outer.pack(fill="both", expand=True)
        outer.columnconfigure(0, weight=1)
        outer.rowconfigure(4, weight=1)

        self._build_inputs(outer).grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self._build_templates(outer).grid(row=1, column=0, sticky="ew", pady=(0, 10))
        self._build_output(outer).grid(row=2, column=0, sticky="ew", pady=(0, 10))
        self._build_actions(outer).grid(row=3, column=0, sticky="ew", pady=(0, 10))
        self._build_report(outer).grid(row=4, column=0, sticky="nsew")

    def _build_inputs(self, parent) -> ttk.Widget:
        frame = ttk.LabelFrame(parent, text=" 1.  QuickBooks export files ",
                               padding=10)
        frame.columnconfigure(0, weight=1)

        self.file_list = tk.Listbox(frame, height=5, selectmode="extended",
                                    activestyle="none")
        self.file_list.grid(row=0, column=0, sticky="ew", rowspan=3)
        scroll = ttk.Scrollbar(frame, orient="vertical",
                               command=self.file_list.yview)
        scroll.grid(row=0, column=1, sticky="ns", rowspan=3)
        self.file_list.configure(yscrollcommand=scroll.set)

        ttk.Button(frame, text="Add files...", command=self.add_files).grid(
            row=0, column=2, sticky="ew", padx=(8, 0))
        ttk.Button(frame, text="Remove", command=self.remove_files).grid(
            row=1, column=2, sticky="ew", padx=(8, 0), pady=4)
        ttk.Button(frame, text="Clear", command=self.clear_files).grid(
            row=2, column=2, sticky="ew", padx=(8, 0))

        ttk.Label(frame, foreground="#444", text=(
            "An .IIF export carries accounts and transactions together. From CSV "
            "reports, add\nboth the General Ledger and the Account Listing — the "
            "listing supplies the account types.")
        ).grid(row=3, column=0, columnspan=3, sticky="w", pady=(8, 0))
        return frame

    def _build_templates(self, parent) -> ttk.Widget:
        frame = ttk.LabelFrame(
            parent, text=" 2.  Drake blank templates  (strongly recommended) ",
            padding=10)
        frame.columnconfigure(1, weight=1)

        for row, (label, var) in enumerate((
            ("Journal Entries:", self.journal_template),
            ("Chart of Accounts:", self.chart_template),
        )):
            ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w",
                                              padx=(0, 8), pady=2)
            ttk.Entry(frame, textvariable=var).grid(row=row, column=1,
                                                    sticky="ew", pady=2)
            ttk.Button(frame, text="Browse...",
                       command=lambda v=var: self.browse_template(v)).grid(
                row=row, column=2, sticky="ew", padx=(8, 0), pady=2)

        ttk.Label(frame, foreground="#444", text=(
            "Get these from Drake Accounting: Tools > Spreadsheets > Export tab. "
            "They pin the output\nto your program year's exact columns. Leave "
            "blank to use the built-in default layout.")
        ).grid(row=2, column=0, columnspan=3, sticky="w", pady=(8, 0))
        return frame

    def _build_output(self, parent) -> ttk.Widget:
        frame = ttk.LabelFrame(parent, text=" 3.  Save the converted files to ",
                               padding=10)
        frame.columnconfigure(0, weight=1)
        ttk.Entry(frame, textvariable=self.out_dir).grid(row=0, column=0, sticky="ew")
        ttk.Button(frame, text="Browse...", command=self.browse_out_dir).grid(
            row=0, column=1, padx=(8, 0))
        return frame

    def _build_actions(self, parent) -> ttk.Widget:
        frame = ttk.LabelFrame(parent, text=" 4.  Options ", padding=10)
        frame.columnconfigure(3, weight=1)

        ttk.Checkbutton(
            frame, variable=self.write_iif,
            text="Also write an .IIF for File > Import > Import QuickBooks"
        ).grid(row=0, column=0, columnspan=4, sticky="w")

        ttk.Checkbutton(
            frame, variable=self.renumber,
            text="Renumber all accounts (ignore QuickBooks' own numbers)"
        ).grid(row=1, column=0, columnspan=4, sticky="w")

        ttk.Label(frame, text="Division:").grid(row=2, column=0, sticky="w",
                                                pady=(6, 0))
        ttk.Entry(frame, textvariable=self.division, width=12).grid(
            row=2, column=1, sticky="w", pady=(6, 0))

        ttk.Label(frame, text="Group ledger rows:").grid(row=2, column=2,
                                                         sticky="e", padx=(16, 6),
                                                         pady=(6, 0))
        ttk.Combobox(frame, textvariable=self.group_by, width=12, state="readonly",
                     values=("auto", "trans-no", "none")).grid(
            row=2, column=3, sticky="w", pady=(6, 0))

        buttons = ttk.Frame(frame)
        buttons.grid(row=3, column=0, columnspan=4, sticky="ew", pady=(12, 0))
        self.convert_button = ttk.Button(buttons, text="Convert",
                                         command=self.start_convert)
        self.convert_button.pack(side="left")
        self.open_button = ttk.Button(buttons, text="Open output folder",
                                      command=self.open_output, state="disabled")
        self.open_button.pack(side="left", padx=8)
        ttk.Button(buttons, text="How do I import these?",
                   command=lambda: TextWindow(self, "Importing into Drake",
                                              IMPORT_HELP)).pack(side="left")
        self.progress = ttk.Progressbar(buttons, mode="indeterminate", length=160)
        self.progress.pack(side="right")
        return frame

    def _build_report(self, parent) -> ttk.Widget:
        frame = ttk.LabelFrame(parent, text=" Result ", padding=8)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        self.report = ScrolledText(frame, wrap="word", height=14,
                                   font=("TkFixedFont", 9))
        self.report.grid(row=0, column=0, sticky="nsew")
        self.report.tag_configure("error", foreground="#b00020")
        self.report.tag_configure("warn", foreground="#8a6100")
        self.report.tag_configure("good", foreground="#006400")
        self.report.tag_configure("head", font=("TkFixedFont", 9, "bold"))
        self.report.configure(state="disabled")
        return frame

    # -------------------------------------------------------------- handlers

    def add_files(self) -> None:
        chosen = filedialog.askopenfilenames(
            title="Choose the QuickBooks export file(s)",
            filetypes=QUICKBOOKS_FILETYPES)
        existing = set(self.file_list.get(0, "end"))
        for path in chosen:
            if path not in existing:
                self.file_list.insert("end", path)
        if chosen:
            self.status.set(f"{self.file_list.size()} file(s) ready to convert.")

    def remove_files(self) -> None:
        for index in reversed(self.file_list.curselection()):
            self.file_list.delete(index)

    def clear_files(self) -> None:
        self.file_list.delete(0, "end")

    def browse_template(self, var: tk.StringVar) -> None:
        path = filedialog.askopenfilename(
            title="Choose the Drake blank template", filetypes=CSV_FILETYPES)
        if path:
            var.set(path)

    def browse_out_dir(self) -> None:
        path = filedialog.askdirectory(title="Choose where to save the files")
        if path:
            self.out_dir.set(path)

    def open_output(self) -> None:
        if not self._last_out_dir or not os.path.isdir(self._last_out_dir):
            return
        try:
            open_in_file_manager(self._last_out_dir)
        except Exception as exc:                        # pragma: no cover - platform
            messagebox.showerror(APP_TITLE, f"Could not open the folder:\n{exc}")

    def collect_options(self) -> JobOptions:
        templates = [path for path in (self.journal_template.get().strip(),
                                       self.chart_template.get().strip()) if path]
        return JobOptions(
            inputs=list(self.file_list.get(0, "end")),
            out_dir=self.out_dir.get().strip(),
            templates=templates,
            division=self.division.get().strip(),
            write_iif=bool(self.write_iif.get()),
            renumber=bool(self.renumber.get()),
            group_by=self.group_by.get() or "auto",
        )

    # --------------------------------------------------------------- running

    def start_convert(self) -> None:
        options = self.collect_options()
        if not options.inputs:
            messagebox.showwarning(APP_TITLE,
                                   "Add at least one QuickBooks export file first.")
            return

        self.convert_button.configure(state="disabled")
        self.open_button.configure(state="disabled")
        self.progress.start(12)
        self.status.set("Converting...")
        self._write_report("Working...\n", [])

        self._worker_thread = threading.Thread(target=self._worker,
                                               args=(options,), daemon=True)
        self._worker_thread.start()
        self._poll_job = self.after(100, self._poll)

    def _worker(self, options: JobOptions) -> None:
        try:
            self._queue.put(run_job(options))
        except Exception as exc:                        # pragma: no cover - safety net
            self._queue.put(JobResult(
                error=f"Something went wrong that the converter did not expect:\n\n"
                      f"{type(exc).__name__}: {exc}"))

    def _poll(self) -> None:
        self._poll_job = None
        try:
            if self._closed or not self.winfo_exists():   # closed mid-conversion
                return
        except tk.TclError:
            return
        try:
            result = self._queue.get_nowait()
        except queue.Empty:
            self._poll_job = self.after(100, self._poll)
            return

        self.progress.stop()
        self.convert_button.configure(state="normal")
        self._show_result(result)

    def wait_for_worker(self, timeout: float = 30.0) -> bool:
        """Block until the conversion thread has finished. Used on close."""
        thread = self._worker_thread
        if thread is None:
            return True
        thread.join(timeout)
        return not thread.is_alive()

    def close(self) -> None:
        """Shut down cleanly even if a conversion is still running.

        Three things have to happen in order, and all of them are things a
        real user triggers by closing the window mid-conversion:

        * cancel our own poll callback,
        * stop the progress bar, which drives its own Tcl timer and will
          otherwise keep firing against a destroyed window,
        * let the worker thread finish -- it never touches a widget, but
          tearing Tcl down underneath a live thread aborts the interpreter.

        Idempotent: the window manager can deliver the close more than once.
        """
        if self._closed:
            return
        self._closed = True

        if self._poll_job is not None:
            try:
                self.after_cancel(self._poll_job)
            except tk.TclError:                 # already fired or gone
                pass
            self._poll_job = None

        try:
            self.progress.stop()
        except tk.TclError:
            pass

        self.wait_for_worker(timeout=5.0)

        try:
            self.destroy()
        except tk.TclError:                     # already gone
            pass

    def _show_result(self, result: JobResult) -> None:
        self._write_report(describe_result(result), self._tag_plan(result))

        if result.error:
            self.status.set("Could not convert. See the message above.")
            return

        self._last_out_dir = os.path.dirname(result.files[0][1]) if result.files else ""
        self.open_button.configure(state="normal" if self._last_out_dir else "disabled")

        if result.error_count:
            self.status.set(
                f"Converted with {result.error_count} problem(s) Drake will "
                "reject. Fix these before importing.")
        elif result.warning_count:
            self.status.set(
                f"Converted. {result.warning_count} warning(s) worth reading.")
        else:
            self.status.set("Converted cleanly. Ready to import into Drake.")

    @staticmethod
    def _tag_plan(result: JobResult) -> list:
        """Which line prefixes get which colour."""
        if result.error:
            return [("", "error")]
        plan = [("ERRORS", "error"), ("WARNINGS", "warn"),
                ("Files written", "head"), ("Next steps", "head"),
                ("Conversion report", "head"),
                ("Template columns", "warn")]
        if result.clean:
            plan.append(("  No problems found.", "good"))
        return plan

    def _write_report(self, text: str, tag_plan: list) -> None:
        self.report.configure(state="normal")
        self.report.delete("1.0", "end")

        active = None
        for line in text.splitlines():
            for prefix, tag in tag_plan:
                if prefix and line.startswith(prefix):
                    active = tag
                    break
                if not prefix:
                    active = tag
            # A blank line ends a coloured block.
            if not line.strip() and active not in (None, "error"):
                active = None
            self.report.insert("end", line + "\n", active or "")

        self.report.configure(state="disabled")
        self.report.see("1.0")


def main() -> int:
    app = ConverterApp()
    app.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
