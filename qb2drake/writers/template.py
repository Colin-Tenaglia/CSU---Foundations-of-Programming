"""Build an output profile from Drake Accounting's own blank template.

Drake ships blank CSV templates for its spreadsheet import (Tools >
Spreadsheets > Export tab gives you e.g. Blank_JournalEntries_Template.csv and
Blank_ChartOfAccounts_Template.csv). Those templates are the authoritative
column layout for the installed program year, so reading the real file beats
guessing at it.

Headers we recognise are wired to a field. Headers we do not recognise are kept
as empty columns in the right position and reported, so the layout still lines
up and you only have to fill in the few we could not place.
"""

from __future__ import annotations

import os
from typing import Dict, List, Tuple

from ..readers.loader import is_blank, load_rows

# Header text (normalised) -> field name, per section.
TRANSACTION_SYNONYMS: Dict[str, str] = {
    "account number": "account_number", "account no": "account_number",
    "account #": "account_number", "acct": "account_number",
    "acct number": "account_number", "acct #": "account_number",
    "account": "account_number", "gl account": "account_number",
    "account name": "account_name", "account description": "account_name",
    "date": "date", "transaction date": "date", "entry date": "date",
    "post date": "date", "posting date": "date",
    "journal": "journal", "journal code": "journal", "jrnl": "journal",
    "reference": "reference", "ref": "reference", "reference number": "reference",
    "ref number": "reference", "ref #": "reference", "invoice": "reference",
    "invoice number": "reference", "document": "reference", "doc": "reference",
    "description": "description", "memo": "description", "desc": "description",
    "transaction description": "description",
    "debit": "debit", "debit amount": "debit", "debits": "debit",
    "credit": "credit", "credit amount": "credit", "credits": "credit",
    "amount": "amount",
    "division": "division", "department": "division", "dept": "division",
    "location": "division",
    "entry": "entry_no", "entry number": "entry_no", "entry no": "entry_no",
    "je number": "entry_no", "transaction number": "entry_no",
    "name": "name", "payee": "name", "vendor": "name", "customer": "name",
}

CHART_SYNONYMS: Dict[str, str] = {
    "level": "level", "account level": "level", "lvl": "level",
    "account number": "number", "account no": "number", "account #": "number",
    "acct number": "number", "acct #": "number", "account": "number",
    "number": "number",
    "description": "description", "account description": "description",
    "name": "description", "account name": "description", "desc": "description",
    "type": "type", "account type": "type", "classification": "type",
    "normal balance": "normal_balance", "balance": "normal_balance",
    "debit/credit": "normal_balance", "dr/cr": "normal_balance",
    "normal": "normal_balance",
    "division": "division", "department": "division", "dept": "division",
    "parent": "parent_number", "parent account": "parent_number",
    "parent number": "parent_number", "parent account number": "parent_number",
    "beginning balance": "opening_balance", "opening balance": "opening_balance",
    "balance forward": "opening_balance",
}

# Headers that mark a template as one kind or the other.
_TRANSACTION_MARKERS = {"debit", "credit", "date", "journal"}
_CHART_MARKERS = {"level", "account type", "normal balance", "type"}


def _normalise(text: str) -> str:
    return " ".join((text or "").strip().lower().replace("_", " ").split())


def read_template_header(path: str) -> List[str]:
    """Return the first non-empty row of a Drake blank template."""
    for row in load_rows(path):
        if not is_blank(row):
            # Trailing empty cells are an artefact of how the file was saved.
            while row and not row[-1]:
                row = row[:-1]
            return row
    raise ValueError(f"{path}: the template has no header row")


def guess_kind(headers: List[str]) -> str:
    """Decide whether a template is the chart or the journal entry layout."""
    normalised = {_normalise(h) for h in headers}
    chart_hits = len(normalised & _CHART_MARKERS)
    transaction_hits = len(normalised & _TRANSACTION_MARKERS)
    if chart_hits > transaction_hits:
        return "chart_of_accounts"
    if transaction_hits > chart_hits:
        return "transactions"
    # "Level" only appears in a chart; debit/credit only in journal entries.
    if "level" in normalised:
        return "chart_of_accounts"
    return "transactions"


def section_from_template(path: str, kind: str = None) -> Tuple[str, dict, List[str]]:
    """Turn a blank template into a profile section.

    Returns (kind, section_dict, unmatched_headers).
    """
    headers = read_template_header(path)
    kind = kind or guess_kind(headers)
    synonyms = CHART_SYNONYMS if kind == "chart_of_accounts" else TRANSACTION_SYNONYMS

    columns, unmatched, used = [], [], set()
    for header in headers:
        field = synonyms.get(_normalise(header))
        if field and field not in used:
            columns.append({"header": header, "field": field})
            used.add(field)
        else:
            # Unknown column, or a second column wanting a field already
            # placed: keep the position, leave the value blank.
            columns.append({"header": header, "constant": ""})
            if header:
                unmatched.append(header)

    section = {
        "filename": os.path.basename(path).replace("Blank_", "").replace("_Template", ""),
        "include_header": True,
        "columns": columns,
    }
    return kind, section, unmatched


def profile_from_templates(paths: List[str]) -> Tuple[dict, Dict[str, List[str]]]:
    """Build a whole profile from one or more Drake blank templates."""
    from .profile import DEFAULT_PROFILE

    profile = {
        "name": "from-drake-template",
        "date_format": "%m/%d/%Y",
        "zero_as_blank": True,
        "chart_of_accounts": dict(DEFAULT_PROFILE["chart_of_accounts"]),
        "transactions": dict(DEFAULT_PROFILE["transactions"]),
    }
    unmatched: Dict[str, List[str]] = {}
    seen = set()

    for path in paths:
        kind, section, missing = section_from_template(path)
        if kind in seen:
            raise ValueError(
                f"{path} looks like another {kind.replace('_', ' ')} template; "
                "pass one template of each kind"
            )
        seen.add(kind)
        profile[kind] = section
        if missing:
            unmatched[path] = missing

    return profile, unmatched
