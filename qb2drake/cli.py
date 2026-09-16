"""Command line interface for qb2drake."""

from __future__ import annotations

import argparse
import csv
import os
import sys
from typing import List

from . import __version__
from .detect import UnsupportedInput, read_many
from .mapping import DEFAULT_RANGES, ChartBuilder, MappingOptions, NORMAL_BALANCE
from .models import sort_transactions
from .validate import validate
from .writers import write_chart_of_accounts, write_transactions
from .writers.profile import dump_profile, load_profile

MAP_HEADER = [
    "quickbooks_account",
    "quickbooks_type",
    "drake_account_number",
    "drake_account_type",
    "drake_description",
    "division",
]


def _parse_ranges(values: List[str]) -> dict:
    ranges = dict(DEFAULT_RANGES)
    for value in values or []:
        if "=" not in value:
            raise SystemExit(f"--range expects TYPE=START[:STEP], got {value!r}")
        account_type, spec = value.split("=", 1)
        account_type = account_type.strip()
        if account_type not in NORMAL_BALANCE:
            raise SystemExit(
                f"--range: unknown account type {account_type!r}; "
                f"choose from {', '.join(NORMAL_BALANCE)}"
            )
        start, _, step = spec.partition(":")
        try:
            ranges[account_type] = (int(start), int(step) if step else 10)
        except ValueError:
            raise SystemExit(f"--range expects whole numbers, got {spec!r}")
    return ranges


def _build_options(args) -> MappingOptions:
    overrides = {}
    if args.account_map:
        if not os.path.exists(args.account_map):
            raise SystemExit(f"account map not found: {args.account_map}")
        overrides = MappingOptions.load_overrides(args.account_map)
    return MappingOptions(
        ranges=_parse_ranges(getattr(args, "range", None)),
        default_type=args.default_type,
        keep_source_numbers=not args.renumber,
        division=args.division,
        overrides=overrides,
    )


def command_convert(args) -> int:
    profile = load_profile(args.profile)
    batch = read_many(args.input, group_by=args.group_by,
                      opening_entry=not args.no_opening_entry)

    builder = ChartBuilder(_build_options(args))
    accounts = builder.build(batch)
    if not args.no_sort:
        batch.transactions = sort_transactions(batch.transactions)

    os.makedirs(args.out_dir, exist_ok=True)
    coa_path = os.path.join(args.out_dir, profile.chart_of_accounts.filename)
    txn_path = os.path.join(args.out_dir, profile.transactions.filename)

    account_rows = write_chart_of_accounts(accounts, coa_path, profile)
    line_rows = write_transactions(batch.transactions, accounts, txn_path, profile,
                                   default_journal=args.default_journal)

    report = validate(batch, accounts)
    report.stats["chart of accounts file"] = coa_path
    report.stats["transactions file"] = txn_path

    text = report.render()
    if args.report:
        with open(args.report, "w", encoding="utf-8") as handle:
            handle.write(text + "\n")
    if not args.quiet:
        print(text)
        print(f"\nWrote {account_rows} account rows to {coa_path}")
        print(f"Wrote {line_rows} journal line rows to {txn_path}")

    if not report.ok:
        if args.strict:
            print("\nErrors found and --strict was set; "
                  "fix the source data and re-run.", file=sys.stderr)
            return 1
        print("\nErrors were found. The files were still written, but Drake "
              "Accounting is likely to reject them until the errors above are "
              "resolved. Re-run with --strict to fail instead.", file=sys.stderr)
    return 0


def command_inspect(args) -> int:
    batch = read_many(args.input, group_by=args.group_by,
                      opening_entry=not args.no_opening_entry)
    accounts = ChartBuilder(_build_options(args)).build(batch)
    print(validate(batch, accounts).render())
    return 0


def command_init_map(args) -> int:
    batch = read_many(args.input, group_by=args.group_by,
                      opening_entry=not args.no_opening_entry)
    accounts = ChartBuilder(_build_options(args)).build(batch)

    with open(args.out, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(MAP_HEADER)
        for account in accounts:
            writer.writerow([
                account.source_name,
                account.qb_type or "",
                account.drake_number or "",
                account.drake_type or "",
                account.description,
                account.division,
            ])
    print(f"Wrote {len(accounts)} accounts to {args.out}")
    print("Edit the drake_* columns as needed, then re-run convert with "
          f"--account-map {args.out}")
    return 0


def command_dump_profile(args) -> int:
    dump_profile(args.out)
    print(f"Wrote the default output layout to {args.out}")
    print("Adjust the columns to match your Drake Accounting import template, "
          "then pass it with --profile.")
    return 0


def _add_shared(parser: argparse.ArgumentParser, *, with_mapping: bool = True) -> None:
    parser.add_argument("input", nargs="+",
                        help="QuickBooks export(s): .iif, .csv, .txt, or .xlsx")
    parser.add_argument("--group-by", choices=("auto", "trans-no", "none"),
                        default="auto",
                        help="how report rows are folded into journal entries "
                             "(default: auto)")
    parser.add_argument("--no-opening-entry", action="store_true",
                        help="for a Trial Balance input, write the chart only and "
                             "skip the opening journal entry")
    if with_mapping:
        parser.add_argument("--account-map",
                            help="CSV of account overrides from `qb2drake init-map`")
        parser.add_argument("--default-type", default="Expense",
                            choices=sorted(NORMAL_BALANCE),
                            help="classification for accounts that cannot be typed")
        parser.add_argument("--renumber", action="store_true",
                            help="ignore QuickBooks account numbers and assign new "
                                 "ones from the type ranges")
        parser.add_argument("--division", default="",
                            help="Drake division to stamp on every row")
        parser.add_argument("--range", action="append", metavar="TYPE=START[:STEP]",
                            help="override the auto-numbering range for one account "
                                 "type, e.g. --range Expense=6000:5 (repeatable)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="qb2drake",
        description="Convert QuickBooks exports into Drake Accounting import files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  qb2drake convert journal.csv -o out/\n"
            "  qb2drake convert accounts.csv gl.csv -o out/\n"
            "  qb2drake init-map export.iif -o accounts.csv\n"
            "  qb2drake convert export.iif --account-map accounts.csv -o out/\n"
        ),
    )
    parser.add_argument("--version", action="version", version=f"qb2drake {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    convert = subparsers.add_parser(
        "convert", help="write the Drake chart of accounts and transaction files")
    _add_shared(convert)
    convert.add_argument("-o", "--out-dir", default="drake_import",
                         help="directory for the generated files (default: drake_import)")
    convert.add_argument("--profile", help="JSON output layout from `qb2drake dump-profile`")
    convert.add_argument("--default-journal", default="GJ",
                         help="journal code for transaction types with no mapping "
                              "(default: GJ)")
    convert.add_argument("--no-sort", action="store_true",
                         help="keep the source file's row order instead of sorting "
                              "entries by date")
    convert.add_argument("--report", help="also write the conversion report to this file")
    convert.add_argument("--strict", action="store_true",
                         help="exit non-zero when the report contains errors")
    convert.add_argument("-q", "--quiet", action="store_true",
                         help="suppress the report on stdout")
    convert.set_defaults(func=command_convert)

    inspect = subparsers.add_parser(
        "inspect", help="parse the input and print the report without writing files")
    _add_shared(inspect)
    inspect.set_defaults(func=command_inspect)

    init_map = subparsers.add_parser(
        "init-map", help="write an editable account mapping CSV")
    _add_shared(init_map)
    init_map.add_argument("-o", "--out", default="account_map.csv",
                          help="where to write the map (default: account_map.csv)")
    init_map.set_defaults(func=command_init_map)

    dump = subparsers.add_parser(
        "dump-profile", help="write the default output layout as JSON for editing")
    dump.add_argument("out", nargs="?", default="drake_profile.json")
    dump.set_defaults(func=command_dump_profile)

    return parser


def main(argv: List[str] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except UnsupportedInput as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
