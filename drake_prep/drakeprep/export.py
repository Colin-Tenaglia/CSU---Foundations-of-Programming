"""Export to the formats Drake can actually ingest.

Drake imports some things and not others. What it accepts, per Drake's own
documentation, includes Forms W-2, 4562, and 8949, Schedules K-1 from a business
return into an individual return, and end-of-year balances. Of those, the 8949
import is the one with a file layout a preparer can produce themselves — a CSV,
TAB, or Excel file through the Form 8949 Import / GruntWorx Trades utility.

So this module does one real export and is honest about the rest:

  8949    a CSV of capital transactions for the 8949 import utility
  csv     every proposed value, flat, for a spreadsheet review
  keying  the Markdown keying sheet (written by `worksheet.py`)

Column order for the 8949 file must be confirmed against the import dialog in your
Drake version before the first use. Import the file, look at what landed where, and
correct COLUMNS below if it differs.
"""

from __future__ import annotations

import csv
from pathlib import Path

from .config import Client, Vault
from .screens import ScreenMap
from .values import Entry, parse_money, parse_date

# Verify against Drake's 8949 import dialog before first use.
COLUMNS_8949 = [
    ("description", "Description of Property"),
    ("date_acquired", "Date Acquired"),
    ("date_sold", "Date Sold"),
    ("proceeds", "Sales Price"),
    ("cost_basis", "Cost or Other Basis"),
    ("adjustment_code", "Adjustment Code"),
    ("adjustment_amount", "Adjustment Amount"),
    ("form8949_box", "Form 8949 Box"),
]


def _money_out(raw: str) -> str:
    amount = parse_money(raw)
    return f"{amount:.2f}" if amount is not None else ""


def _date_out(raw: str) -> str:
    parsed = parse_date(raw)
    return parsed.strftime("%m/%d/%Y") if parsed else str(raw or "")


def export_8949(vault: Vault, client: Client, entries: list[Entry]) -> tuple[Path, int]:
    rows = [e for e in entries if e.screen.upper() == "8949" and e.values]
    path = vault.sub(client.slug, "out") / f"{client.slug}_8949.csv"
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow([label for _fid, label in COLUMNS_8949])
        for e in rows:
            out = []
            for fid, _label in COLUMNS_8949:
                raw = e.values.get(fid, "")
                if fid in ("proceeds", "cost_basis", "adjustment_amount"):
                    out.append(_money_out(raw))
                elif fid in ("date_acquired", "date_sold"):
                    out.append(_date_out(raw))
                else:
                    out.append(str(raw))
            w.writerow(out)
    path.chmod(0o600)
    return path, len(rows)


def export_flat_csv(vault: Vault, client: Client, smap: ScreenMap,
                    entries: list[Entry]) -> tuple[Path, int]:
    """Every proposed value, one row each, unmasked money and text but with
    identifier fields left out. For a spreadsheet review before keying."""
    path = vault.sub(client.slug, "out") / f"{client.slug}_values.csv"
    skip_types = {"ssn", "ein", "account"}
    count = 0
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["screen", "instance", "wp_ref", "source_doc", "box", "field_id",
                    "label", "type", "value", "confidence"])
        for e in sorted(entries, key=lambda e: (e.screen, e.instance)):
            screen = smap.by_code(e.screen)
            if screen is None:
                continue
            for f in screen.fields:
                raw = e.values.get(f.id, "")
                if not str(raw).strip() or f.type in skip_types:
                    continue
                w.writerow([screen.code, e.instance, e.wp_ref or "", e.source_doc,
                            f.box, f.id, f.label, f.type, raw,
                            e.confidence.get(f.id, "")])
                count += 1
    path.chmod(0o600)
    return path, count


NOT_SUPPORTED = {
    "w2": ("Drake imports W-2s, but the file layout is not published for preparers "
           "to generate. Key from the keying sheet, or use Drake's own W-2 import "
           "against a payroll provider it supports."),
    "4562": ("Drake imports Form 4562 asset detail, but the layout is not published. "
             "Key from the keying sheet."),
    "k1": ("Drake exports a K-1 from a business return directly into an individual "
           "return. Use that path rather than a file — it is inside Drake and does "
           "not involve this desk."),
}
