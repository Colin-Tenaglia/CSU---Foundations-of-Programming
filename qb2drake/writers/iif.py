"""Write a chart of accounts as an .IIF file.

Drake Accounting's built-in File > Import > Import QuickBooks wizard accepts an
IIF file and nothing else -- the file must even carry the .IIF extension. That
is fine when the source is QuickBooks Desktop, which exports IIF natively, but
QuickBooks Online has no IIF export at all. Writing IIF here lets an Online
export (or any report CSV) reach that wizard.

Two things this fixes on the way through:

* Drake's own instructions tell you to switch on "Use Account Numbers" in
  QuickBooks before exporting, because the import needs numbered accounts.
  A file that was exported without them imports as an unusable chart. Every
  account written here has a number, assigned if QuickBooks had none.
* Opening balances are written as zero on purpose. Balances belong in the
  journal entry import; carrying them on the accounts as well would post
  them twice.
"""

from __future__ import annotations

from typing import List

from ..mapping import (ASSET, COST_OF_SALES, EQUITY, EXPENSE, INCOME,
                       LIABILITY, OTHER_EXPENSE, OTHER_INCOME)
from ..models import Account

# The header QuickBooks itself writes, so the file looks like a native export.
ACCNT_HEADER = ["!ACCNT", "NAME", "REFNUM", "TIMESTAMP", "ACCNTTYPE",
                "OBAMOUNT", "DESC", "ACCNUM", "SCD"]

# Valid IIF account type codes. A source code in this set is passed straight
# through, which keeps Bank a Bank rather than flattening it to a generic asset.
VALID_IIF_CODES = {
    "BANK", "AR", "OCASSET", "FIXASSET", "OASSET", "AP", "CCARD", "OCLIAB",
    "LTLIAB", "OLIAB", "EQUITY", "INC", "COGS", "EXP", "EXINC", "EXEXP",
}

# Fallback when the source had no usable IIF code.
CLASS_TO_IIF = {
    ASSET: "OCASSET",
    LIABILITY: "OCLIAB",
    EQUITY: "EQUITY",
    INCOME: "INC",
    COST_OF_SALES: "COGS",
    EXPENSE: "EXP",
    OTHER_INCOME: "EXINC",
    OTHER_EXPENSE: "EXEXP",
}

# Report wording -> the IIF code QuickBooks would have used, so a report-sourced
# chart keeps the same detail an IIF export would have had.
REPORT_TO_IIF = {
    "bank": "BANK",
    "cash and cash equivalents": "BANK",
    "accounts receivable": "AR",
    "accounts receivable (a/r)": "AR",
    "other current asset": "OCASSET",
    "other current assets": "OCASSET",
    "inventory": "OCASSET",
    "fixed asset": "FIXASSET",
    "fixed assets": "FIXASSET",
    "other asset": "OASSET",
    "other assets": "OASSET",
    "accounts payable": "AP",
    "accounts payable (a/p)": "AP",
    "credit card": "CCARD",
    "other current liability": "OCLIAB",
    "other current liabilities": "OCLIAB",
    "long term liability": "LTLIAB",
    "long-term liability": "LTLIAB",
    "long term liabilities": "LTLIAB",
    "other liability": "OLIAB",
    "equity": "EQUITY",
    "income": "INC",
    "revenue": "INC",
    "sales": "INC",
    "cost of goods sold": "COGS",
    "cost of sales": "COGS",
    "expense": "EXP",
    "expenses": "EXP",
    "other income": "EXINC",
    "other expense": "EXEXP",
}


def iif_type(account: Account) -> str:
    """Pick the IIF account type code for an account."""
    raw = (account.qb_type or "").strip()
    if raw.upper() in VALID_IIF_CODES:
        return raw.upper()
    mapped = REPORT_TO_IIF.get(raw.lower())
    if mapped:
        return mapped
    return CLASS_TO_IIF.get(account.drake_type, "EXP")


def _clean(text: str) -> str:
    """IIF is tab delimited, so tabs and newlines cannot survive in a value."""
    return (text or "").replace("\t", " ").replace("\r", " ").replace("\n", " ").strip()


def write_iif(accounts: List[Account], path: str) -> int:
    """Write the chart of accounts as an IIF file. Returns the row count."""
    lines = ["\t".join(ACCNT_HEADER)]
    for index, account in enumerate(accounts, start=1):
        lines.append("\t".join([
            "ACCNT",
            _clean(account.source_name),
            str(index),
            "0",
            iif_type(account),
            "0.00",
            _clean(account.description),
            _clean(account.drake_number or ""),
            "",
        ]))

    with open(path, "w", newline="", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    return len(accounts)
