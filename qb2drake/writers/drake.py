"""Render the mapped data as Drake Accounting import CSV files."""

from __future__ import annotations

import csv
from decimal import Decimal
from typing import Dict, Iterable, List, Optional

from ..mapping import journal_code
from ..models import Account, Transaction, ZERO
from .profile import Column, Profile, Section


def _amount(value: Decimal, profile: Profile) -> str:
    if value == ZERO and profile.zero_as_blank:
        return ""
    return f"{value:.2f}"


def _write(path: str, section: Section, rows: Iterable[List[str]]) -> int:
    count = 0
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        if section.include_header:
            writer.writerow([column.header for column in section.columns])
        for row in rows:
            writer.writerow(row)
            count += 1
    return count


def _render(columns: List[Column], values: Dict[str, str]) -> List[str]:
    out = []
    for column in columns:
        if column.constant:
            out.append(column.constant)
        else:
            out.append(values.get(column.field, ""))
    return out


def write_chart_of_accounts(accounts: List[Account], path: str, profile: Profile) -> int:
    section = profile.chart_of_accounts
    by_name = {account.source_name: account for account in accounts}

    def rows():
        for account in accounts:
            parent = by_name.get(account.parent_name or "")
            yield _render(section.columns, {
                "level": str(account.level),
                "number": account.drake_number or "",
                "description": account.description,
                "type": account.drake_type or "",
                "normal_balance": account.normal_balance,
                "division": account.division,
                "parent_number": (parent.drake_number or "") if parent else "",
                "source_name": account.source_name,
                "opening_balance": _amount(account.opening_balance, profile),
            })

    return _write(path, section, rows())


def write_transactions(transactions: List[Transaction], accounts: List[Account],
                       path: str, profile: Profile,
                       default_journal: str = "GJ") -> int:
    section = profile.transactions
    numbers = {account.source_name: (account.drake_number or "") for account in accounts}

    def rows():
        for index, transaction in enumerate(transactions, start=1):
            journal = transaction.journal
            if not journal or journal == "GJ":
                journal = journal_code(transaction.source_type, default_journal)
            date_text = (transaction.date.strftime(profile.date_format)
                         if transaction.date else "")
            for line in transaction.lines:
                yield _render(section.columns, {
                    "entry_no": str(index),
                    "date": date_text,
                    "journal": journal,
                    "reference": transaction.reference,
                    "account_number": numbers.get(line.account, ""),
                    "account_name": line.account,
                    "description": line.memo or transaction.description,
                    "memo": line.memo,
                    "name": line.name,
                    "debit": _amount(line.debit, profile),
                    "credit": _amount(line.credit, profile),
                    "amount": f"{line.signed_amount:.2f}",
                    "division": line.division,
                })

    return _write(path, section, rows())
