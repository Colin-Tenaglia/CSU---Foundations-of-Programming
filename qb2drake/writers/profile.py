"""Output layout definition.

Drake Accounting's import templates differ between program years, and a firm
can also re-order the columns in the import wizard. Rather than bake one
layout into the code, the column list lives in a JSON profile that can be
dumped, edited, and passed back in with --profile.

Run `qb2drake dump-profile my.json`, line the columns up with the template
your copy of Drake Accounting expects, then `qb2drake convert --profile my.json`.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List

# Field names a column may reference. Keep in sync with writers/drake.py.
CHART_FIELDS = (
    "level", "number", "description", "type", "normal_balance", "division",
    "parent_number", "source_name", "opening_balance",
)
TRANSACTION_FIELDS = (
    "entry_no", "date", "journal", "reference", "account_number",
    "account_name", "description", "memo", "name", "debit", "credit",
    "amount", "division",
)

DEFAULT_PROFILE: Dict[str, Any] = {
    "name": "drake-accounting-default",
    "date_format": "%m/%d/%Y",
    "zero_as_blank": True,
    "chart_of_accounts": {
        "filename": "drake_chart_of_accounts.csv",
        "include_header": True,
        "columns": [
            {"header": "Level", "field": "level"},
            {"header": "Account Number", "field": "number"},
            {"header": "Account Description", "field": "description"},
            {"header": "Account Type", "field": "type"},
            {"header": "Normal Balance", "field": "normal_balance"},
            {"header": "Division", "field": "division"},
        ],
    },
    "transactions": {
        "filename": "drake_transactions.csv",
        "include_header": True,
        "columns": [
            {"header": "Date", "field": "date"},
            {"header": "Journal", "field": "journal"},
            {"header": "Reference", "field": "reference"},
            {"header": "Account Number", "field": "account_number"},
            {"header": "Description", "field": "description"},
            {"header": "Debit", "field": "debit"},
            {"header": "Credit", "field": "credit"},
            {"header": "Division", "field": "division"},
        ],
    },
}


@dataclass
class Column:
    header: str
    field: str
    constant: str = ""          # emit this fixed text instead of a field

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Column":
        return cls(
            header=data.get("header", ""),
            field=data.get("field", ""),
            constant=data.get("constant", ""),
        )


@dataclass
class Section:
    filename: str
    columns: List[Column] = field(default_factory=list)
    include_header: bool = True

    @classmethod
    def from_dict(cls, data: Dict[str, Any], default_filename: str) -> "Section":
        return cls(
            filename=data.get("filename", default_filename),
            columns=[Column.from_dict(c) for c in data.get("columns", [])],
            include_header=bool(data.get("include_header", True)),
        )


@dataclass
class Profile:
    name: str = "drake-accounting-default"
    date_format: str = "%m/%d/%Y"
    zero_as_blank: bool = True
    chart_of_accounts: Section = None
    transactions: Section = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Profile":
        profile = cls(
            name=data.get("name", "custom"),
            date_format=data.get("date_format", "%m/%d/%Y"),
            zero_as_blank=bool(data.get("zero_as_blank", True)),
            chart_of_accounts=Section.from_dict(
                data.get("chart_of_accounts", {}), "drake_chart_of_accounts.csv"),
            transactions=Section.from_dict(
                data.get("transactions", {}), "drake_transactions.csv"),
        )
        profile.validate()
        return profile

    @classmethod
    def default(cls) -> "Profile":
        return cls.from_dict(DEFAULT_PROFILE)

    def validate(self) -> None:
        problems = []
        for section, allowed in (
            (self.chart_of_accounts, CHART_FIELDS),
            (self.transactions, TRANSACTION_FIELDS),
        ):
            if section is None:
                continue
            for column in section.columns:
                if column.constant:
                    continue
                # A column with neither field nor constant is a deliberate
                # placeholder: it holds a position in the layout and writes
                # nothing. `profile-from-template` emits these for template
                # columns it could not match.
                if not column.field:
                    continue
                if column.field not in allowed:
                    problems.append(
                        f"{section.filename}: unknown field {column.field!r} "
                        f"(choose from {', '.join(allowed)})"
                    )
        if problems:
            raise ValueError("profile is not valid:\n  " + "\n  ".join(problems))


def load_profile(path: str = None) -> Profile:
    if not path:
        return Profile.default()
    with open(path, encoding="utf-8") as handle:
        return Profile.from_dict(json.load(handle))


def dump_profile(path: str) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(DEFAULT_PROFILE, handle, indent=2)
        handle.write("\n")
