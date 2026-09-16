"""Intermediate representation shared by every reader and writer.

QuickBooks exports and Drake Accounting imports have nothing in common
structurally, so everything funnels through these objects: readers produce
them, mapping enriches them, writers consume them.
"""

from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Iterable, Optional

TWOPLACES = Decimal("0.01")
ZERO = Decimal("0.00")


def money(value) -> Decimal:
    """Coerce anything QuickBooks might emit into a 2-place Decimal."""
    if value is None or value == "":
        return ZERO
    if isinstance(value, Decimal):
        return value.quantize(TWOPLACES)
    if isinstance(value, (int, float)):
        return Decimal(str(value)).quantize(TWOPLACES)

    text = str(value).strip()
    if not text:
        return ZERO

    negative = False
    # Reports render negatives as (1,234.56); IIF uses a leading minus.
    if text.startswith("(") and text.endswith(")"):
        negative = True
        text = text[1:-1]
    text = text.replace(",", "").replace("$", "").replace(" ", "")
    if text.startswith("-"):
        negative = not negative
        text = text[1:]
    if text.startswith("+"):
        text = text[1:]
    if not text:
        return ZERO

    try:
        amount = Decimal(text).quantize(TWOPLACES)
    except Exception as exc:  # pragma: no cover - guarded by callers
        raise ValueError(f"cannot parse amount {value!r}") from exc
    return -amount if negative else amount


@dataclass
class Account:
    """One node of the chart of accounts."""

    source_name: str                      # full QuickBooks name, e.g. "Bank:Checking"
    description: str = ""
    qb_type: Optional[str] = None         # raw QuickBooks type string
    number: Optional[str] = None          # QuickBooks account number, if any
    opening_balance: Decimal = ZERO

    # Filled in by qb2drake.mapping
    drake_number: Optional[str] = None
    drake_type: Optional[str] = None      # Asset / Liability / Equity / ...
    normal_balance: str = "D"             # "D" or "C"
    level: int = 1
    division: str = ""

    @property
    def parent_name(self) -> Optional[str]:
        if ":" not in self.source_name:
            return None
        return self.source_name.rsplit(":", 1)[0]

    @property
    def leaf_name(self) -> str:
        return self.source_name.rsplit(":", 1)[-1]

    @property
    def depth(self) -> int:
        return self.source_name.count(":") + 1


@dataclass
class JournalLine:
    """A single debit-or-credit posting inside a transaction."""

    account: str                          # QuickBooks account name as exported
    debit: Decimal = ZERO
    credit: Decimal = ZERO
    memo: str = ""
    name: str = ""                        # customer / vendor / employee
    division: str = ""

    @property
    def signed_amount(self) -> Decimal:
        return self.debit - self.credit

    @classmethod
    def from_signed(cls, account: str, amount: Decimal, **kwargs) -> "JournalLine":
        """Build a line from an IIF-style signed amount (positive = debit)."""
        amount = money(amount)
        if amount >= ZERO:
            return cls(account=account, debit=amount, credit=ZERO, **kwargs)
        return cls(account=account, debit=ZERO, credit=-amount, **kwargs)


@dataclass
class Transaction:
    """A balanced set of journal lines sharing one date and reference."""

    date: Optional[_dt.date] = None
    journal: str = "GJ"
    reference: str = ""
    description: str = ""
    source_type: str = ""                 # QuickBooks transaction type, for journal mapping
    lines: list[JournalLine] = field(default_factory=list)

    @property
    def total_debit(self) -> Decimal:
        return sum((l.debit for l in self.lines), ZERO)

    @property
    def total_credit(self) -> Decimal:
        return sum((l.credit for l in self.lines), ZERO)

    @property
    def out_of_balance(self) -> Decimal:
        return (self.total_debit - self.total_credit).quantize(TWOPLACES)

    @property
    def is_balanced(self) -> bool:
        return self.out_of_balance == ZERO

    def accounts(self) -> Iterable[str]:
        return (l.account for l in self.lines)


@dataclass
class Batch:
    """Everything one QuickBooks file yielded."""

    accounts: list[Account] = field(default_factory=list)
    transactions: list[Transaction] = field(default_factory=list)
    source_format: str = "unknown"
    source_path: str = ""
    notes: list[str] = field(default_factory=list)

    def account_names(self) -> set[str]:
        names = {a.source_name for a in self.accounts}
        for txn in self.transactions:
            names.update(txn.accounts())
        names.discard("")
        return names

    def merge(self, other: "Batch") -> "Batch":
        known = {a.source_name for a in self.accounts}
        for account in other.accounts:
            if account.source_name not in known:
                self.accounts.append(account)
                known.add(account.source_name)
        self.transactions.extend(other.transactions)
        self.notes.extend(other.notes)
        return self


def sort_transactions(transactions: list) -> list:
    """Order entries by date, keeping same-day entries in source order.

    QuickBooks General Ledger exports are ordered by account, so the entries
    come out of the reader interleaved. Undated entries sort last so they are
    easy to spot in the output file.
    """
    far_future = _dt.date(9999, 12, 31)
    return sorted(transactions, key=lambda t: t.date or far_future)
