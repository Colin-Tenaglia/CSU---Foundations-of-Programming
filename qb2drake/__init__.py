"""qb2drake -- convert QuickBooks exports into Drake Accounting import files.

Typical use::

    from qb2drake import convert
    result = convert(["journal.csv"], "drake_import/")
    print(result.report.render())
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Optional

__version__ = "1.0.0"

__all__ = ["convert", "ConversionResult", "__version__"]


@dataclass
class ConversionResult:
    accounts: list
    transactions: list
    report: object
    chart_path: str
    transactions_path: str


def convert(inputs: List[str], out_dir: str, *,
            profile_path: Optional[str] = None,
            account_map: Optional[str] = None,
            group_by: str = "auto",
            opening_entry: bool = True,
            division: str = "",
            default_journal: str = "GJ",
            sort_by_date: bool = True) -> ConversionResult:
    """Convert QuickBooks export(s) and write the Drake import files."""
    from .detect import read_many
    from .mapping import ChartBuilder, MappingOptions
    from .models import sort_transactions
    from .validate import validate
    from .writers import write_chart_of_accounts, write_transactions
    from .writers.profile import load_profile

    profile = load_profile(profile_path)
    batch = read_many(inputs, group_by=group_by, opening_entry=opening_entry)

    options = MappingOptions(division=division)
    if account_map:
        options.overrides = MappingOptions.load_overrides(account_map)
    accounts = ChartBuilder(options).build(batch)
    if sort_by_date:
        batch.transactions = sort_transactions(batch.transactions)

    os.makedirs(out_dir, exist_ok=True)
    chart_path = os.path.join(out_dir, profile.chart_of_accounts.filename)
    transactions_path = os.path.join(out_dir, profile.transactions.filename)
    write_chart_of_accounts(accounts, chart_path, profile)
    write_transactions(batch.transactions, accounts, transactions_path, profile,
                       default_journal=default_journal)

    return ConversionResult(
        accounts=accounts,
        transactions=batch.transactions,
        report=validate(batch, accounts),
        chart_path=chart_path,
        transactions_path=transactions_path,
    )
