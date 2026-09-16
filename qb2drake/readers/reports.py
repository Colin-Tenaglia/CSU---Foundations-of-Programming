"""Parser for QuickBooks report exports (Desktop and Online, CSV or Excel).

These files are laid out for a human reader, not a machine: title rows above
the real header, a leading blank column, subtotal rows mixed in with detail,
and -- in a General Ledger -- the account printed once as a section heading
rather than on every row. This module normalises all of that.

Supported reports
-----------------
Journal / Transaction Detail   flat rows, one account per row
General Ledger                 rows grouped under account section headings
Trial Balance                  account with a debit or credit balance
Account Listing / Chart of Accounts   account metadata only
"""

from __future__ import annotations

import datetime as _dt
from typing import Dict, List, Optional, Tuple

from ..dates import find_report_date, parse_date
from ..models import Account, Batch, JournalLine, Transaction, ZERO, money
from .loader import is_blank

# Normalised header text -> canonical field name. Covers Desktop and Online
# wording for the same column.
COLUMN_ALIASES: Dict[str, str] = {}


def _alias(field: str, *labels: str) -> None:
    for label in labels:
        COLUMN_ALIASES[label] = field


_alias("trans_no", "trans #", "trans#", "transaction #", "entry no", "entry no.",
       "je no", "je no.", "journal no", "journal no.", "transaction id")
_alias("date", "date", "trans date", "transaction date", "posting date", "txn date")
_alias("txn_type", "type", "transaction type", "trans type", "txn type")
_alias("num", "num", "no.", "number", "doc num", "docnum", "ref", "ref no.",
       "ref number", "reference", "reference no.", "check #", "check no.")
_alias("name", "name", "vendor", "customer", "payee", "customer/vendor",
       "employee", "customer/project", "vendor/payee")
_alias("memo", "memo", "description", "memo/description", "memo / description",
       "memo/desc")
_alias("account", "account", "account name", "account full name", "full account name")
_alias("split", "split", "split account")
_alias("debit", "debit", "debits", "debit amount")
_alias("credit", "credit", "credits", "credit amount")
_alias("amount", "amount", "amount (usd)", "amount usd")
_alias("balance", "balance", "running balance", "balance total", "total")
_alias("acct_num", "accnt. #", "accnt #", "account #", "acct #", "acct. #",
       "account number", "account no.")
_alias("acct_type", "account type", "type of account")
_alias("acct_desc", "account description")
_alias("division", "class", "location", "department", "division")
_alias("adj", "adj", "adj.")

MONEY_FIELDS = ("debit", "credit", "amount")

# Sentinel key meaning "this row belongs to whatever entry preceded it".
_CONTINUE = "\x00continue"


def _normalise(label: str) -> str:
    return " ".join((label or "").strip().lower().split())


def _map_header(row: List[str]) -> Dict[str, int]:
    """Map canonical field names to column indexes for one candidate row."""
    mapping: Dict[str, int] = {}
    for index, cell in enumerate(row):
        key = _normalise(cell)
        if not key:
            continue
        field = COLUMN_ALIASES.get(key)
        if field and field not in mapping:
            mapping[field] = index
    return mapping


def find_header(rows: List[List[str]], search_limit: int = 30) -> Tuple[int, Dict[str, int]]:
    """Locate the real header row and its column mapping.

    Returns (-1, {}) when nothing in the file looks like a report header.
    """
    best_index, best_map, best_score = -1, {}, 0
    for index, row in enumerate(rows[:search_limit]):
        if is_blank(row):
            continue
        mapping = _map_header(row)
        score = len(mapping)
        # A lone "Description"/"Total" column is a title, not a header.
        if score >= 2 and score > best_score:
            best_index, best_map, best_score = index, mapping, score
    return best_index, best_map


def classify_report(columns: Dict[str, int]) -> str:
    has = columns.__contains__
    money_columns = has("debit") or has("credit") or has("amount")

    if has("date") and money_columns:
        return "transactions"
    if (has("debit") or has("credit")) and not has("date"):
        return "trial_balance"
    if has("acct_type") or has("acct_num") or (has("account") and has("balance")):
        return "account_listing"
    if money_columns:
        return "trial_balance"
    return "unknown"


def _cell(row: List[str], columns: Dict[str, int], field: str, default: str = "") -> str:
    index = columns.get(field)
    if index is None or index >= len(row):
        return default
    return row[index] or default


def _first_text(row: List[str]) -> str:
    for cell in row:
        if cell:
            return cell
    return ""


def _is_total_row(row: List[str]) -> bool:
    text = _normalise(_first_text(row))
    return text.startswith("total") or text in ("net income", "gross profit", "net ordinary income")


def _row_has_money(row: List[str], columns: Dict[str, int]) -> bool:
    return any(_cell(row, columns, field) for field in MONEY_FIELDS)


def parse_report(rows: List[List[str]], path: str = "", *,
                 group_by: str = "auto", opening_entry: bool = True) -> Batch:
    """Parse any supported QuickBooks report into a Batch."""
    header_index, columns = find_header(rows)
    if header_index < 0:
        raise ValueError(
            f"{path or 'input'}: could not find a recognisable header row. "
            "Export the report again with 'Comma Delimited File' selected."
        )

    kind = classify_report(columns)
    body = rows[header_index + 1:]
    preamble = rows[:header_index]

    if kind == "transactions":
        batch = _parse_transactions(body, columns, group_by=group_by)
    elif kind == "trial_balance":
        batch = _parse_trial_balance(body, columns, preamble,
                                     opening_entry=opening_entry)
    elif kind == "account_listing":
        batch = _parse_account_listing(body, columns)
    else:
        raise ValueError(
            f"{path or 'input'}: header row recognised but the report type is not "
            "supported. Use a Journal, General Ledger, Trial Balance, or Account "
            "Listing report."
        )

    batch.source_path = path
    batch.source_format = f"report:{kind}"
    return batch


# --------------------------------------------------------------------------
# Journal / General Ledger
# --------------------------------------------------------------------------

def _parse_transactions(body: List[List[str]], columns: Dict[str, int],
                        *, group_by: str = "auto") -> Batch:
    batch = Batch()
    grouped = "account" not in columns      # General Ledger style
    section_account = ""
    amount_only = "amount" in columns and "debit" not in columns and "credit" not in columns
    if amount_only:
        batch.notes.append(
            "report has a signed Amount column instead of Debit/Credit; "
            "positive amounts were treated as debits"
        )

    entries: List[Tuple[str, JournalLine, Transaction]] = []

    for row in body:
        if is_blank(row):
            continue
        if _is_total_row(row):
            continue

        date = parse_date(_cell(row, columns, "date"))
        if date is None and not _row_has_money(row, columns):
            # An account section heading in a General Ledger.
            heading = _first_text(row)
            if grouped and heading:
                section_account = heading
            continue

        if grouped:
            account = (row[0] if row and row[0] else "") or section_account
        else:
            account = _cell(row, columns, "account") or section_account
        if not account:
            batch.notes.append(f"row skipped, no account could be determined: {row}")
            continue

        if amount_only:
            line = JournalLine.from_signed(
                account,
                _cell(row, columns, "amount"),
                memo=_cell(row, columns, "memo"),
                name=_cell(row, columns, "name"),
                division=_cell(row, columns, "division"),
            )
        else:
            debit = money(_cell(row, columns, "debit"))
            credit = money(_cell(row, columns, "credit"))
            # Reports occasionally put a negative in the debit column.
            if debit < ZERO:
                credit, debit = credit - debit, ZERO
            if credit < ZERO:
                debit, credit = debit - credit, ZERO
            line = JournalLine(
                account=account,
                debit=debit,
                credit=credit,
                memo=_cell(row, columns, "memo"),
                name=_cell(row, columns, "name"),
                division=_cell(row, columns, "division"),
            )

        if line.debit == ZERO and line.credit == ZERO:
            continue

        header = Transaction(
            date=date,
            source_type=_cell(row, columns, "txn_type"),
            reference=_cell(row, columns, "num"),
            description=_cell(row, columns, "memo") or _cell(row, columns, "name"),
        )
        key = _group_key(row, columns, header, grouped, group_by)
        entries.append((key, line, header))

    batch.transactions = _assemble(entries)
    return batch


def _group_key(row: List[str], columns: Dict[str, int], header: Transaction,
               grouped: bool, group_by: str) -> str:
    """Decide which rows belong to the same journal entry."""
    if group_by == "none":
        return f"row:{id(row)}"

    # A Journal report numbers every entry, which makes grouping exact.
    if "trans_no" in columns and group_by in ("trans-no", "auto"):
        trans_no = _cell(row, columns, "trans_no")
        return f"trans:{trans_no}" if trans_no else _CONTINUE
    if group_by == "trans-no":
        return _CONTINUE

    # Flat reports print the date once per entry and leave it blank on the
    # remaining lines of that entry.
    if not grouped and header.date is None:
        return _CONTINUE

    # A General Ledger prints each side under its own account section, so the
    # entry has to be rebuilt from the columns both sides share.
    return "|".join([
        header.date.isoformat() if header.date else "",
        (header.source_type or "").lower(),
        header.reference or "",
        (_cell(row, columns, "name") or "").lower(),
    ])


def _assemble(entries) -> List[Transaction]:
    """Fold (key, line, header) tuples into transactions, preserving order."""
    order: List[str] = []
    by_key: Dict[str, Transaction] = {}
    previous_key: Optional[str] = None

    for key, line, header in entries:
        if key == _CONTINUE:                 # continuation of the previous entry
            key = previous_key or "orphan"
        if key not in by_key:
            by_key[key] = header
            order.append(key)
        else:
            existing = by_key[key]
            if existing.date is None:
                existing.date = header.date
            if not existing.reference:
                existing.reference = header.reference
            if not existing.source_type:
                existing.source_type = header.source_type
            if not existing.description:
                existing.description = header.description
        by_key[key].lines.append(line)
        previous_key = key

    return [by_key[key] for key in order]


# --------------------------------------------------------------------------
# Trial Balance
# --------------------------------------------------------------------------

def _parse_trial_balance(body: List[List[str]], columns: Dict[str, int],
                         preamble: List[List[str]], *, opening_entry: bool) -> Batch:
    batch = Batch()
    as_of = find_report_date(preamble)
    lines: List[JournalLine] = []

    for row in body:
        if is_blank(row) or _is_total_row(row):
            continue
        account = _cell(row, columns, "account") or _first_text(row)
        if not account:
            continue
        debit = money(_cell(row, columns, "debit"))
        credit = money(_cell(row, columns, "credit"))

        # A zero-balance account still belongs in the chart; it just has no
        # opening entry line.
        batch.accounts.append(
            Account(
                source_name=account,
                description=account.rsplit(":", 1)[-1],
                qb_type=_cell(row, columns, "acct_type") or None,
                number=_cell(row, columns, "acct_num") or None,
                opening_balance=debit - credit,
            )
        )
        if debit != ZERO or credit != ZERO:
            lines.append(JournalLine(account=account, debit=debit, credit=credit,
                                     memo="Opening balance"))

    if opening_entry and lines:
        batch.transactions.append(
            Transaction(
                date=as_of or _dt.date.today(),
                journal="GJ",
                reference="TB",
                description="Trial balance opening entry",
                source_type="Journal Entry",
                lines=lines,
            )
        )
    return batch


# --------------------------------------------------------------------------
# Account Listing
# --------------------------------------------------------------------------

def _parse_account_listing(body: List[List[str]], columns: Dict[str, int]) -> Batch:
    batch = Batch()
    for row in body:
        if is_blank(row) or _is_total_row(row):
            continue
        account = _cell(row, columns, "account") or _first_text(row)
        if not account:
            continue
        batch.accounts.append(
            Account(
                source_name=account,
                description=(_cell(row, columns, "acct_desc")
                         or _cell(row, columns, "memo")
                         or account.rsplit(":", 1)[-1]),
                qb_type=_cell(row, columns, "acct_type") or _cell(row, columns, "txn_type") or None,
                number=_cell(row, columns, "acct_num") or None,
                opening_balance=money(_cell(row, columns, "balance")),
            )
        )
    return batch
