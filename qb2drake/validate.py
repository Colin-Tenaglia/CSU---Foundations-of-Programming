"""Checks that run between reading and writing.

Drake Accounting rejects an import wholesale when something is wrong with it,
and the error it reports is rarely specific. It is much cheaper to find the
problems here, against the QuickBooks source, than in the import wizard.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from decimal import Decimal
from typing import List

from .models import Account, Batch, Transaction, ZERO


@dataclass
class Report:
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    stats: dict = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.errors

    def render(self) -> str:
        lines = ["Conversion report", "=" * 17, ""]
        for key, value in self.stats.items():
            lines.append(f"  {key:.<34} {value}")
        for label, items in (("ERRORS", self.errors), ("WARNINGS", self.warnings)):
            if items:
                lines.extend(["", f"{label} ({len(items)})", "-" * len(label)])
                lines.extend(f"  - {item}" for item in items)
        if self.ok and not self.warnings:
            lines.extend(["", "  No problems found."])
        return "\n".join(lines)


def _describe(transaction: Transaction) -> str:
    date = transaction.date.isoformat() if transaction.date else "no date"
    reference = transaction.reference or "no ref"
    return f"{date} / {reference} / {transaction.source_type or 'entry'}"


def validate(batch: Batch, accounts: List[Account], *,
             max_listed: int = 25) -> Report:
    report = Report()
    total_debit = sum((t.total_debit for t in batch.transactions), ZERO)
    total_credit = sum((t.total_credit for t in batch.transactions), ZERO)
    line_count = sum(len(t.lines) for t in batch.transactions)

    report.stats = {
        "source format": batch.source_format,
        "accounts written": len(accounts),
        "transactions written": len(batch.transactions),
        "journal lines written": line_count,
        "total debits": f"{total_debit:,.2f}",
        "total credits": f"{total_credit:,.2f}",
        "difference": f"{total_debit - total_credit:,.2f}",
    }

    unbalanced = [t for t in batch.transactions if not t.is_balanced]
    if unbalanced:
        report.errors.append(
            f"{len(unbalanced)} transaction(s) do not balance; Drake will reject these"
        )
        for transaction in unbalanced[:max_listed]:
            report.errors.append(
                f"    out of balance by {transaction.out_of_balance:,.2f}: "
                f"{_describe(transaction)}"
            )
        if len(unbalanced) > max_listed:
            report.errors.append(f"    ... and {len(unbalanced) - max_listed} more")

    undated = [t for t in batch.transactions if t.date is None]
    if undated:
        report.errors.append(
            f"{len(undated)} transaction(s) have no usable date "
            f"(first: {_describe(undated[0])})"
        )

    empty = [t for t in batch.transactions if not t.lines]
    if empty:
        report.warnings.append(f"{len(empty)} transaction(s) had no journal lines and were dropped")

    numbers = Counter(a.drake_number for a in accounts if a.drake_number)
    duplicates = [number for number, count in numbers.items() if count > 1]
    if duplicates:
        report.errors.append(
            "duplicate Drake account numbers: " + ", ".join(sorted(duplicates)[:max_listed])
        )

    missing_number = [a.source_name for a in accounts if not a.drake_number]
    if missing_number:
        report.errors.append(
            "accounts without a Drake account number: "
            + ", ".join(missing_number[:max_listed])
        )

    known = {a.source_name for a in accounts}
    orphans = sorted({line.account for t in batch.transactions for line in t.lines} - known)
    if orphans:
        report.errors.append(
            "transactions reference accounts missing from the chart: "
            + ", ".join(orphans[:max_listed])
        )

    untyped = [a.source_name for a in accounts if not a.qb_type]
    if untyped:
        report.warnings.append(
            f"{len(untyped)} account(s) had no QuickBooks type; their Drake type was "
            "inferred from the parent account or the account name -- review these: "
            + ", ".join(untyped[:max_listed])
        )

    deep = [a.source_name for a in accounts if a.depth > 4]
    if deep:
        report.warnings.append(
            "account nesting deeper than Drake's 4 levels was flattened to level 4: "
            + ", ".join(deep[:max_listed])
        )

    for note in batch.notes[:max_listed]:
        report.warnings.append(note)
    if len(batch.notes) > max_listed:
        report.warnings.append(f"... and {len(batch.notes) - max_listed} more notes")

    return report
