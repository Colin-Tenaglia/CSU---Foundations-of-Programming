"""Parser for QuickBooks Desktop .IIF interchange files.

An IIF file interleaves several record types, each introduced by a header
line beginning with "!". We care about two of them:

    !ACCNT  ...   chart of accounts
    !TRNS / !SPL / !ENDTRNS   transactions

Within a transaction the TRNS line carries one side of the entry and each SPL
line carries the other; amounts are signed so that the whole transaction sums
to zero, with positive meaning debit.
"""

from __future__ import annotations

from typing import List, Optional

from ..dates import parse_date
from ..models import Account, Batch, JournalLine, Transaction, money
from .loader import load_rows


def _field(row: List[str], headers: List[str], name: str, default: str = "") -> str:
    try:
        index = headers.index(name)
    except ValueError:
        return default
    return row[index] if index < len(row) else default


def parse_iif(path: str) -> Batch:
    rows = load_rows(path)
    batch = Batch(source_format="iif", source_path=path)

    headers: dict = {}
    current: Optional[Transaction] = None

    for row in rows:
        if not row or not row[0]:
            continue
        tag = row[0].upper()

        if tag.startswith("!"):
            headers[tag[1:]] = [cell.upper() for cell in row[1:]]
            continue

        if tag == "ACCNT":
            fields = headers.get("ACCNT", [])
            name = _field(row[1:], fields, "NAME")
            if not name:
                continue
            batch.accounts.append(
                Account(
                    source_name=name,
                    description=_field(row[1:], fields, "DESC") or name.rsplit(":", 1)[-1],
                    qb_type=_field(row[1:], fields, "ACCNTTYPE") or None,
                    number=_field(row[1:], fields, "ACCNUM") or None,
                    opening_balance=money(_field(row[1:], fields, "OBAMOUNT")),
                )
            )

        elif tag == "TRNS":
            if current is not None:            # file omitted ENDTRNS
                batch.transactions.append(current)
            current = _start_transaction(row[1:], headers.get("TRNS", []))

        elif tag == "SPL":
            if current is None:
                batch.notes.append("SPL record encountered outside a transaction; skipped")
                continue
            line = _make_line(row[1:], headers.get("SPL", []))
            if line is not None:
                current.lines.append(line)

        elif tag == "ENDTRNS":
            if current is not None:
                batch.transactions.append(current)
                current = None

    if current is not None:
        batch.transactions.append(current)

    return batch


def _start_transaction(row: List[str], fields: List[str]) -> Transaction:
    transaction = Transaction(
        date=parse_date(_field(row, fields, "DATE")),
        source_type=_field(row, fields, "TRNSTYPE"),
        reference=_field(row, fields, "DOCNUM"),
        description=_field(row, fields, "MEMO") or _field(row, fields, "NAME"),
    )
    line = _make_line(row, fields)
    if line is not None:
        transaction.lines.append(line)
    return transaction


def _make_line(row: List[str], fields: List[str]) -> Optional[JournalLine]:
    account = _field(row, fields, "ACCNT")
    if not account:
        return None
    return JournalLine.from_signed(
        account,
        _field(row, fields, "AMOUNT"),
        memo=_field(row, fields, "MEMO"),
        name=_field(row, fields, "NAME"),
        division=_field(row, fields, "CLASS"),
    )
