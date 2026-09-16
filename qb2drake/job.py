"""One conversion, start to finish, with no user interface attached.

The GUI and the command line both need the same sequence: work out the output
layout, read the inputs, build the chart, write the files, validate. Keeping it
here means the GUI holds no accounting logic and can be tested without a
display.
"""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .detect import UnsupportedInput, read_many
from .mapping import ChartBuilder, MappingOptions
from .models import sort_transactions
from .validate import validate
from .writers import write_chart_of_accounts, write_iif, write_transactions
from .writers.profile import Profile, load_profile
from .writers.template import profile_from_templates


@dataclass
class JobOptions:
    inputs: List[str] = field(default_factory=list)
    out_dir: str = "drake_import"

    # Output layout: templates win over an explicit profile, which wins over
    # the built-in default.
    templates: List[str] = field(default_factory=list)
    profile_path: Optional[str] = None

    account_map: Optional[str] = None
    division: str = ""
    write_iif: bool = False
    renumber: bool = False
    group_by: str = "auto"
    opening_entry: bool = True
    default_type: str = "Expense"
    default_journal: str = "GJ"
    sort_by_date: bool = True


@dataclass
class JobResult:
    ok: bool = False
    error: Optional[str] = None            # set when the job could not run at all
    report_text: str = ""
    files: List[Tuple[str, str]] = field(default_factory=list)   # (label, path)
    unmatched_columns: Dict[str, List[str]] = field(default_factory=dict)
    error_count: int = 0
    warning_count: int = 0

    @property
    def clean(self) -> bool:
        """Ran, and Drake should accept what came out."""
        return self.ok and self.error_count == 0


NEXT_STEPS = """\
Next steps in Drake Accounting
------------------------------
Chart of accounts and journal entries:
    Tools > Spreadsheets > Import tab
    Pick the type on the left, browse to the matching file above, wait for
    "Properties Detected" to fill in, then Check all required fields > Import.

If you also produced an .IIF file:
    File > Import > Import QuickBooks
    Choose the .IIF and enter a Client Code. The Client Code is not in your
    QuickBooks data -- you choose it. Up to 8 letters, digits or underscores.
    A code that does not exist yet creates a new client; an existing one takes
    only what that client is missing.

Each selection imports once per client, so review the report above before
importing rather than planning to re-import over the top.\
"""


def resolve_profile(options: JobOptions) -> Tuple[Profile, Dict[str, List[str]], Optional[str]]:
    """Return (profile, unmatched columns, temporary profile path if written)."""
    if options.templates:
        profile_dict, unmatched = profile_from_templates(options.templates)
        handle = tempfile.NamedTemporaryFile(
            "w", suffix=".json", delete=False, encoding="utf-8")
        with handle:
            json.dump(profile_dict, handle, indent=2)
        return Profile.from_dict(profile_dict), unmatched, handle.name
    return load_profile(options.profile_path), {}, None


def run_job(options: JobOptions) -> JobResult:
    """Run a conversion. Never raises for ordinary user error."""
    result = JobResult()

    if not options.inputs:
        result.error = "Choose at least one QuickBooks export file to convert."
        return result
    if not options.out_dir:
        result.error = "Choose a folder to save the converted files into."
        return result

    try:
        profile, unmatched, _ = resolve_profile(options)
        result.unmatched_columns = unmatched

        batch = read_many(options.inputs, group_by=options.group_by,
                          opening_entry=options.opening_entry)

        mapping = MappingOptions(
            default_type=options.default_type,
            keep_source_numbers=not options.renumber,
            division=options.division,
        )
        if options.account_map:
            mapping.overrides = MappingOptions.load_overrides(options.account_map)

        accounts = ChartBuilder(mapping).build(batch)
        if options.sort_by_date:
            batch.transactions = sort_transactions(batch.transactions)

        os.makedirs(options.out_dir, exist_ok=True)
        chart_path = os.path.join(options.out_dir, profile.chart_of_accounts.filename)
        txn_path = os.path.join(options.out_dir, profile.transactions.filename)

        write_chart_of_accounts(accounts, chart_path, profile)
        write_transactions(batch.transactions, accounts, txn_path, profile,
                           default_journal=options.default_journal)
        result.files = [("Chart of Accounts", chart_path),
                        ("Journal Entries", txn_path)]

        if options.write_iif:
            # Drake's Import QuickBooks wizard rejects any other extension.
            iif_path = os.path.join(options.out_dir, "drake_chart_of_accounts.IIF")
            write_iif(accounts, iif_path)
            result.files.append(("Chart of Accounts (IIF)", iif_path))

        report = validate(batch, accounts)
        result.error_count = len(report.errors)
        result.warning_count = len(report.warnings)
        result.report_text = report.render()
        result.ok = True

    except UnsupportedInput as exc:
        result.error = str(exc)
    except (ValueError, OSError) as exc:
        result.error = str(exc)

    return result


def describe_result(result: JobResult) -> str:
    """The full text shown to someone after a run."""
    if result.error:
        return result.error

    parts = [result.report_text, ""]

    if result.unmatched_columns:
        parts.append("Template columns that could not be matched")
        parts.append("-" * 42)
        for path, headers in result.unmatched_columns.items():
            parts.append(f"  {os.path.basename(path)}:")
            for header in headers:
                parts.append(f"    - {header}")
        parts.append("  These are left blank in the right position. If Drake needs")
        parts.append("  one filled in, say so and it can be mapped.")
        parts.append("")

    parts.append("Files written")
    parts.append("-" * 13)
    for label, path in result.files:
        parts.append(f"  {label:.<28} {path}")
    parts.extend(["", NEXT_STEPS])
    return "\n".join(parts)
