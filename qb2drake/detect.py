"""Work out what kind of QuickBooks export a file is, then read it."""

from __future__ import annotations

import os
from typing import List

from .models import Batch
from .readers import load_rows, parse_iif, parse_report

IIF_TAGS = {
    "!HDR", "!ACCNT", "!TRNS", "!SPL", "!ENDTRNS", "!CUST", "!VEND",
    "!CLASS", "!INVITEM", "!EMP", "!OTHERNAME", "!TIMEACT",
}


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
