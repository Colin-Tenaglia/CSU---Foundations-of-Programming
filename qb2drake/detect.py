"""Work out what kind of QuickBooks export a file is, then read it."""

from __future__ import annotations

import os
from typing import List

from .models import Batch
from .readers import load_rows, parse_iif, parse_report


class UnsupportedInput(ValueError):
    """Raised for a file that is recognisably QuickBooks but cannot be read.

    Kept separate from a parse failure so the CLI can print the instructions
    for getting an export it *can* read, rather than a parser error.
    """


# Proprietary QuickBooks files. These are binary containers with no published
# format; only QuickBooks itself can open them.
COMPANY_FILES = {
    ".qbb": "QuickBooks backup file",
    ".qbw": "QuickBooks company file",
    ".qbm": "QuickBooks portable company file",
    ".qbx": "Accountant's Copy transfer file",
    ".qba": "Accountant's Copy working file",
    ".qby": "Accountant's Copy import file",
    ".des": "QuickBooks form template",
    ".nd": "QuickBooks network descriptor file",
    ".tlg": "QuickBooks transaction log file",
}

RESTORE_AND_EXPORT = """
Restore it in QuickBooks Desktop first, then export something this tool reads:

  1. File > Open or Restore Company > Restore a backup copy
  2. Then EITHER
       File > Utilities > Export > Lists to IIF Files
       (tick "Chart of Accounts" -- this gives you accounts, not transactions)
     OR, for transactions as well:
       Reports > Accountant & Taxes > General Ledger   (set the date range)
       Excel > Create New Worksheet > Export to a comma separated values (.csv) file
       ...and do the same for Reports > Accountant & Taxes > Account Listing
  3. Run qb2drake against the .iif / .csv files you exported.

No QuickBooks Desktop available? The file has to be opened by some copy of
QuickBooks -- send it to whoever prepared it and ask for a General Ledger and
an Account Listing exported to CSV, or for an IIF export.
"""


def _binary_sample(path: str, size: int = 8192) -> bytes:
    with open(path, "rb") as handle:
        return handle.read(size)

IIF_TAGS = {
    "!HDR", "!ACCNT", "!TRNS", "!SPL", "!ENDTRNS", "!CUST", "!VEND",
    "!CLASS", "!INVITEM", "!EMP", "!OTHERNAME", "!TIMEACT",
}


def check_readable(path: str) -> None:
    """Reject QuickBooks files we cannot read, with instructions.

    Raises UnsupportedInput; callers that just want to parse can ignore it and
    let the reader fail on its own.
    """
    extension = os.path.splitext(path)[1].lower()

    if extension in COMPANY_FILES:
        raise UnsupportedInput(
            f"{path} is a {COMPANY_FILES[extension]} ({extension}).\n\n"
            "That is a proprietary binary format with no published specification, "
            "so no tool outside QuickBooks can read it -- qb2drake included.\n"
            + RESTORE_AND_EXPORT
        )

    if extension == ".qbo":
        raise UnsupportedInput(
            f"{path} is a QuickBooks Web Connect file (.qbo).\n\n"
            "That is a bank or credit card statement download, not accounting "
            "data: it has one side of each transaction and no chart of accounts, "
            "so there is nothing to build a Drake import from. Import it into "
            "QuickBooks, categorise the transactions, then export a General "
            "Ledger or Journal report and convert that."
        )

    if extension in (".xlsx", ".xlsm"):
        return                                   # legitimately binary

    # Catch a renamed company file, or any other binary handed to us by
    # mistake, before the parser produces a confusing message about headers.
    if b"\x00" in _binary_sample(path):
        raise UnsupportedInput(
            f"{path} is a binary file, not a text export.\n\n"
            "qb2drake reads IIF files and CSV / TSV / XLSX report exports. If "
            "this is a QuickBooks company or backup file that has been renamed, "
            "it still has to be opened in QuickBooks and exported."
            + RESTORE_AND_EXPORT
        )


def sniff(path: str, rows: List[List[str]] = None) -> str:
    """Return 'iif' or 'report'."""
    if os.path.splitext(path)[1].lower() == ".iif":
        return "iif"
    sample = (rows if rows is not None else load_rows(path))[:40]
    for row in sample:
        if row and row[0].upper() in IIF_TAGS:
            return "iif"
    return "report"


def read(path: str, *, group_by: str = "auto", opening_entry: bool = True) -> Batch:
    """Read any supported QuickBooks export into a Batch."""
    if not os.path.exists(path):
        raise SystemExit(f"input file not found: {path}")
    check_readable(path)

    if os.path.splitext(path)[1].lower() == ".iif":
        return parse_iif(path)

    rows = load_rows(path)
    if sniff(path, rows) == "iif":
        return parse_iif(path)
    return parse_report(rows, path, group_by=group_by, opening_entry=opening_entry)


def read_many(paths: List[str], **kwargs) -> Batch:
    """Read several exports (e.g. an account listing plus a journal) as one."""
    combined = Batch(source_format="combined")
    formats = []
    for path in paths:
        batch = read(path, **kwargs)
        formats.append(f"{os.path.basename(path)}={batch.source_format}")
        combined.merge(batch)
    combined.source_path = ", ".join(paths)
    combined.source_format = "; ".join(formats)
    return combined
