"""Translate QuickBooks account semantics into Drake Accounting semantics.

Two jobs live here:

1. Account *type* translation. QuickBooks has ~15 account types (and IIF uses
   its own short codes); Drake Accounting groups them into a handful of
   classifications with a normal balance.
2. Account *number* assignment. Drake requires a numeric account number, but
   QuickBooks files frequently carry none (numbering is off by default). We
   assign numbers deterministically from type-based ranges so that re-running
   the converter on the same input always produces the same chart.
"""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass, field
from typing import Optional

from .models import Account, Batch, ZERO

# Drake classifications used throughout.
ASSET = "Asset"
LIABILITY = "Liability"
EQUITY = "Equity"
INCOME = "Income"
COST_OF_SALES = "Cost of Sales"
EXPENSE = "Expense"
OTHER_INCOME = "Other Income"
OTHER_EXPENSE = "Other Expense"

NORMAL_BALANCE = {
    ASSET: "D",
    LIABILITY: "C",
    EQUITY: "C",
    INCOME: "C",
    COST_OF_SALES: "D",
    EXPENSE: "D",
    OTHER_INCOME: "C",
    OTHER_EXPENSE: "D",
}

# IIF short codes (QuickBooks Desktop) -> Drake classification.
IIF_TYPES = {
    "BANK": ASSET,
    "AR": ASSET,
    "OCASSET": ASSET,
    "FIXASSET": ASSET,
    "OASSET": ASSET,
    "AP": LIABILITY,
    "CCARD": LIABILITY,
    "OCLIAB": LIABILITY,
    "LTLIAB": LIABILITY,
    "OLIAB": LIABILITY,
    "EQUITY": EQUITY,
    "INC": INCOME,
    "COGS": COST_OF_SALES,
    "EXP": EXPENSE,
    "EXINC": OTHER_INCOME,
    "EXEXP": OTHER_EXPENSE,
    "NONPOSTING": None,          # estimates / purchase orders: never imported
}

# Long-form type names as they appear in QuickBooks report CSV exports
# (Desktop "Account Listing" and QuickBooks Online "Chart of Accounts").
REPORT_TYPES = {
    "bank": ASSET,
    "cash and cash equivalents": ASSET,
    "accounts receivable": ASSET,
    "accounts receivable (a/r)": ASSET,
    "other current asset": ASSET,
    "other current assets": ASSET,
    "fixed asset": ASSET,
    "fixed assets": ASSET,
    "other asset": ASSET,
    "other assets": ASSET,
    "inventory": ASSET,
    "accounts payable": LIABILITY,
    "accounts payable (a/p)": LIABILITY,
    "credit card": LIABILITY,
    "other current liability": LIABILITY,
    "other current liabilities": LIABILITY,
    "long term liability": LIABILITY,
    "long-term liability": LIABILITY,
    "long term liabilities": LIABILITY,
    "other liability": LIABILITY,
    "equity": EQUITY,
    "income": INCOME,
    "revenue": INCOME,
    "sales": INCOME,
    "service/fee income": INCOME,
    "cost of goods sold": COST_OF_SALES,
    "cost of sales": COST_OF_SALES,
    "expense": EXPENSE,
    "expenses": EXPENSE,
    "other income": OTHER_INCOME,
    "other expense": OTHER_EXPENSE,
    "non-posting": None,
}

# Starting number and step for each classification when auto-numbering.
DEFAULT_RANGES = {
    ASSET: (1000, 10),
    LIABILITY: (2000, 10),
    EQUITY: (3000, 10),
    INCOME: (4000, 10),
    COST_OF_SALES: (5000, 10),
    EXPENSE: (6000, 10),
    OTHER_INCOME: (7000, 10),
    OTHER_EXPENSE: (8000, 10),
}

# QuickBooks transaction types -> Drake journal codes. Anything unlisted
# falls through to the general journal.
JOURNAL_CODES = {
    "check": "CD",
    "bill payment": "CD",
    "bill payment (check)": "CD",
    "bill pmt -check": "CD",
    "bill pmt -credit card": "CD",
    "paycheck": "PR",
    "payroll check": "PR",
    "liability check": "PR",
    "deposit": "CR",
    "payment": "CR",
    "sales receipt": "CR",
    "receive payment": "CR",
    "invoice": "SJ",
    "credit memo": "SJ",
    "sales tax payment": "CD",
    "bill": "PJ",
    "vendor credit": "PJ",
    "item receipt": "PJ",
    "credit card charge": "CD",
    "credit card credit": "CD",
    "journal entry": "GJ",
    "journal": "GJ",
    "general journal": "GJ",
    "transfer": "GJ",
    "inventory adjustment": "GJ",
}

_NON_NUMERIC = re.compile(r"[^0-9]")


def classify(raw_type: Optional[str]) -> Optional[str]:
    """Map a QuickBooks type (IIF code or report label) to a Drake class."""
    if not raw_type:
        return None
    key = raw_type.strip()
    if key.upper() in IIF_TYPES:
        return IIF_TYPES[key.upper()]
    return REPORT_TYPES.get(key.lower())


def journal_code(transaction_type: Optional[str], default: str = "GJ") -> str:
    if not transaction_type:
        return default
    return JOURNAL_CODES.get(transaction_type.strip().lower(), default)


@dataclass
class MappingOptions:
    """Knobs that control chart-of-accounts generation."""

    ranges: dict = field(default_factory=lambda: dict(DEFAULT_RANGES))
    default_type: str = EXPENSE
    max_level: int = 4
    keep_source_numbers: bool = True
    division: str = ""
    overrides: dict = field(default_factory=dict)   # source name -> {number, type, description}

    @classmethod
    def load_overrides(cls, path: str) -> dict:
        """Read an account-map CSV produced by `qb2drake init-map`."""
        overrides: dict = {}
        with open(path, newline="", encoding="utf-8-sig") as handle:
            for row in csv.DictReader(handle):
                name = (row.get("quickbooks_account") or "").strip()
                if not name:
                    continue
                entry = {}
                for src, dest in (
                    ("drake_account_number", "number"),
                    ("drake_account_type", "type"),
                    ("drake_description", "description"),
                    ("division", "division"),
                ):
                    value = (row.get(src) or "").strip()
                    if value:
                        entry[dest] = value
                if entry:
                    overrides[name] = entry
        return overrides


class ChartBuilder:
    """Builds the finished Drake chart of accounts from a Batch."""

    def __init__(self, options: Optional[MappingOptions] = None):
        self.options = options or MappingOptions()
        self.unmapped_types: set = set()

    def build(self, batch: Batch) -> list[Account]:
        accounts = {a.source_name: a for a in batch.accounts}

        # Accounts referenced by transactions but absent from any account list.
        for name in sorted(batch.account_names()):
            if name not in accounts:
                accounts[name] = Account(source_name=name, description=name.rsplit(":", 1)[-1])
                batch.notes.append(f"account inferred from transactions: {name}")

        # Every parent implied by a "Parent:Child" name must exist in Drake.
        for name in list(accounts):
            parts = name.split(":")
            for depth in range(1, len(parts)):
                parent = ":".join(parts[:depth])
                if parent not in accounts:
                    child_type = accounts[name].qb_type
                    accounts[parent] = Account(
                        source_name=parent,
                        description=parts[depth - 1],
                        qb_type=child_type,
                    )
                    batch.notes.append(f"parent account created: {parent}")

        ordered = sorted(accounts.values(), key=lambda a: (a.source_name.lower(),))
        self._assign_types(ordered, accounts)
        self._assign_levels(ordered)
        self._assign_numbers(ordered)
        return sorted(ordered, key=_sort_key)

    def _assign_types(self, ordered: list[Account], index: dict) -> None:
        for account in ordered:
            override = self.options.overrides.get(account.source_name, {})
            drake_type = override.get("type") or classify(account.qb_type)

            # A sub-account inherits its parent's classification when its own
            # type is missing -- QuickBooks GL exports often omit it.
            if not drake_type:
                parent = account.parent_name
                while parent and not drake_type:
                    parent_account = index.get(parent)
                    if parent_account is None:
                        break
                    drake_type = classify(parent_account.qb_type)
                    parent = parent_account.parent_name

            if not drake_type:
                drake_type = _guess_from_name(account.source_name)
            if not drake_type:
                if account.qb_type:
                    self.unmapped_types.add(account.qb_type)
                drake_type = self.options.default_type

            account.drake_type = drake_type
            account.normal_balance = NORMAL_BALANCE.get(drake_type, "D")
            if override.get("description"):
                account.description = override["description"]
            elif not account.description:
                account.description = account.leaf_name
            account.division = override.get("division") or self.options.division

    def _assign_levels(self, ordered: list[Account]) -> None:
        for account in ordered:
            account.level = min(account.depth, self.options.max_level)

    def _assign_numbers(self, ordered: list[Account]) -> None:
        taken: set = set()
        pending: list[Account] = []

        for account in ordered:
            override = self.options.overrides.get(account.source_name, {})
            number = override.get("number")
            if not number and self.options.keep_source_numbers and account.number:
                number = _NON_NUMERIC.sub("", str(account.number)) or None
            if number and number in taken:
                pending.append(account)      # duplicate: fall back to auto-assign
                continue
            if number:
                account.drake_number = number
                taken.add(number)
            else:
                pending.append(account)

        cursors = {}
        for account in pending:
            drake_type = account.drake_type or self.options.default_type
            start, step = self.options.ranges.get(drake_type, (9000, 10))
            cursor = cursors.get(drake_type, start)
            while str(cursor) in taken:
                cursor += step
            account.drake_number = str(cursor)
            taken.add(str(cursor))
            cursors[drake_type] = cursor + step


def _guess_from_name(name: str) -> Optional[str]:
    """Last-resort classification for typeless accounts, by name keyword."""
    lowered = name.lower()
    keywords = [
        (ASSET, ("cash", "checking", "savings", "bank", "receivable", "inventory",
                 "prepaid", "equipment", "furniture", "vehicle", "accumulated depreciation",
                 "undeposited")),
        (LIABILITY, ("payable", "loan", "note payable", "credit card", "accrued",
                     "payroll liab", "sales tax", "deferred")),
        (EQUITY, ("equity", "capital", "retained earnings", "draw", "distribution",
                  "common stock", "opening balance")),
        (INCOME, ("income", "revenue", "sales", "fees earned")),
        (COST_OF_SALES, ("cost of goods", "cost of sales", "cogs", "purchases")),
        (EXPENSE, ("expense", "rent", "utilities", "insurance", "wages", "salaries",
                   "supplies", "advertising", "depreciation expense")),
    ]
    for drake_type, words in keywords:
        if any(word in lowered for word in words):
            return drake_type
    return None


def _sort_key(account: Account):
    number = account.drake_number or ""
    return (len(number), number, account.source_name.lower())
