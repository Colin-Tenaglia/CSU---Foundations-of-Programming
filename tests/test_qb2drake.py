"""Tests for the QuickBooks -> Drake Accounting converter.

Run with:  python -m unittest discover -s tests -v
"""

from __future__ import annotations

import csv
import datetime as _dt
import os
import sys
import tempfile
import unittest
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qb2drake import convert
from qb2drake.detect import read, read_many, sniff
from qb2drake.mapping import ChartBuilder, MappingOptions, classify, journal_code
from qb2drake.models import Account, Batch, JournalLine, Transaction, money
from qb2drake.readers.reports import classify_report, find_header, parse_report
from qb2drake.validate import validate
from qb2drake.writers.profile import Profile

SAMPLES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "samples")


def sample(name: str) -> str:
    return os.path.join(SAMPLES, name)


def read_csv(path: str):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.reader(handle))


class MoneyTests(unittest.TestCase):
    def test_report_formatting_is_understood(self):
        self.assertEqual(money("1,234.56"), Decimal("1234.56"))
        self.assertEqual(money("$1,234.56"), Decimal("1234.56"))
        self.assertEqual(money("(1,234.56)"), Decimal("-1234.56"))
        self.assertEqual(money("-45"), Decimal("-45.00"))
        self.assertEqual(money(""), Decimal("0.00"))
        self.assertEqual(money(None), Decimal("0.00"))

    def test_parenthesised_negative_is_not_double_negated(self):
        self.assertEqual(money("(-5.00)"), Decimal("5.00"))

    def test_signed_line_picks_the_right_column(self):
        self.assertEqual(JournalLine.from_signed("Cash", "100").debit, Decimal("100.00"))
        self.assertEqual(JournalLine.from_signed("Cash", "100").credit, Decimal("0.00"))
        self.assertEqual(JournalLine.from_signed("Cash", "-100").credit, Decimal("100.00"))


class DetectionTests(unittest.TestCase):
    def test_iif_detected_by_content_not_just_extension(self):
        self.assertEqual(sniff(sample("quickbooks_export.iif")), "iif")
        self.assertEqual(sniff(sample("journal.csv")), "report")

    def test_report_kinds(self):
        expected = {
            "journal.csv": "report:transactions",
            "general_ledger.csv": "report:transactions",
            "trial_balance.csv": "report:trial_balance",
            "account_listing.csv": "report:account_listing",
            "qbo_journal.csv": "report:transactions",
        }
        for name, kind in expected.items():
            with self.subTest(name=name):
                self.assertEqual(read(sample(name)).source_format, kind)

    def test_header_row_is_found_below_the_title_block(self):
        from qb2drake.readers.loader import load_rows
        index, columns = find_header(load_rows(sample("journal.csv")))
        self.assertEqual(index, 3)
        self.assertIn("trans_no", columns)
        self.assertIn("debit", columns)

    def test_unrecognisable_input_raises_a_useful_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "junk.csv")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("hello\nworld\n")
            with self.assertRaises(ValueError) as caught:
                read(path)
            self.assertIn("header row", str(caught.exception))

    def test_classify_report_needs_a_date_for_transactions(self):
        self.assertEqual(classify_report({"date": 0, "debit": 1, "credit": 2}), "transactions")
        self.assertEqual(classify_report({"debit": 1, "credit": 2}), "trial_balance")
        self.assertEqual(classify_report({"account": 0, "acct_num": 1}), "account_listing")


class IIFTests(unittest.TestCase):
    def setUp(self):
        self.batch = read(sample("quickbooks_export.iif"))

    def test_accounts_and_transactions_are_read(self):
        self.assertEqual(len(self.batch.accounts), 10)
        self.assertEqual(len(self.batch.transactions), 5)

    def test_every_transaction_balances(self):
        for transaction in self.batch.transactions:
            with self.subTest(ref=transaction.reference):
                self.assertTrue(transaction.is_balanced, transaction)

    def test_signs_are_translated_to_debit_and_credit(self):
        check = self.batch.transactions[0]
        self.assertEqual(check.date, _dt.date(2025, 1, 15))
        by_account = {line.account: line for line in check.lines}
        self.assertEqual(by_account["Checking"].credit, Decimal("245.80"))
        self.assertEqual(by_account["Utilities:Electric"].debit, Decimal("245.80"))

    def test_account_metadata_survives(self):
        checking = next(a for a in self.batch.accounts if a.source_name == "Checking")
        self.assertEqual(checking.qb_type, "BANK")
        self.assertEqual(checking.number, "1010")
        self.assertEqual(checking.description, "Operating checking account")


class GeneralLedgerTests(unittest.TestCase):
    """The GL prints each side of an entry under its own account heading."""

    def setUp(self):
        self.batch = read(sample("general_ledger.csv"))

    def test_sides_are_reassembled_into_whole_entries(self):
        self.assertEqual(len(self.batch.transactions), 3)
        for transaction in self.batch.transactions:
            with self.subTest(ref=transaction.reference):
                self.assertEqual(len(transaction.lines), 2)
                self.assertTrue(transaction.is_balanced)

    def test_section_heading_becomes_the_account(self):
        accounts = {line.account for t in self.batch.transactions for line in t.lines}
        self.assertEqual(
            accounts,
            {"Checking", "Accounts Receivable", "Consulting Income", "Utilities:Electric"},
        )

    def test_subtotal_and_grand_total_rows_are_ignored(self):
        total = sum(line.debit for t in self.batch.transactions for line in t.lines)
        self.assertEqual(total, Decimal("5245.80"))

    def test_group_by_none_keeps_rows_separate(self):
        from qb2drake.readers.loader import load_rows
        batch = parse_report(load_rows(sample("general_ledger.csv")), group_by="none")
        self.assertEqual(len(batch.transactions), 6)


class JournalReportTests(unittest.TestCase):
    def test_trans_number_groups_the_entry(self):
        batch = read(sample("journal.csv"))
        self.assertEqual(len(batch.transactions), 4)
        self.assertTrue(all(t.is_balanced for t in batch.transactions))
        self.assertEqual(batch.transactions[0].reference, "1001")

    def test_qbo_blank_date_continues_the_previous_entry(self):
        batch = read(sample("qbo_journal.csv"))
        self.assertEqual(len(batch.transactions), 2)
        for transaction in batch.transactions:
            self.assertEqual(len(transaction.lines), 2)
            self.assertTrue(transaction.is_balanced)
        self.assertEqual(batch.transactions[0].date, _dt.date(2025, 1, 15))


class TrialBalanceTests(unittest.TestCase):
    def setUp(self):
        self.batch = read(sample("trial_balance.csv"))

    def test_opening_entry_balances_and_is_dated_as_of(self):
        self.assertEqual(len(self.batch.transactions), 1)
        entry = self.batch.transactions[0]
        self.assertTrue(entry.is_balanced)
        self.assertEqual(entry.date, _dt.date(2025, 1, 31))
        self.assertEqual(entry.total_debit, Decimal("4310.00"))

    def test_zero_balance_account_still_reaches_the_chart(self):
        names = {a.source_name for a in self.batch.accounts}
        self.assertIn("Accounts Receivable", names)
        zero = next(a for a in self.batch.accounts if a.source_name == "Accounts Receivable")
        self.assertEqual(zero.opening_balance, Decimal("0.00"))

    def test_opening_entry_can_be_suppressed(self):
        batch = read(sample("trial_balance.csv"), opening_entry=False)
        self.assertEqual(batch.transactions, [])
        self.assertTrue(batch.accounts)


class AccountListingTests(unittest.TestCase):
    def test_types_numbers_and_descriptions_are_read(self):
        batch = read(sample("account_listing.csv"))
        by_name = {a.source_name: a for a in batch.accounts}
        self.assertEqual(by_name["Checking"].qb_type, "Bank")
        self.assertEqual(by_name["Checking"].number, "1010")
        self.assertEqual(by_name["Checking"].description, "Operating checking account")
        self.assertEqual(by_name["Interest Income"].qb_type, "Other Income")


class ClassificationTests(unittest.TestCase):
    def test_iif_codes(self):
        self.assertEqual(classify("BANK"), "Asset")
        self.assertEqual(classify("CCARD"), "Liability")
        self.assertEqual(classify("COGS"), "Cost of Sales")
        self.assertEqual(classify("EXINC"), "Other Income")

    def test_report_labels_including_qbo_wording(self):
        self.assertEqual(classify("Other Current Liability"), "Liability")
        self.assertEqual(classify("Accounts Receivable (A/R)"), "Asset")
        self.assertEqual(classify("Cost of Goods Sold"), "Cost of Sales")

    def test_unknown_type_is_not_guessed_here(self):
        self.assertIsNone(classify("Wibble"))
        self.assertIsNone(classify(None))

    def test_journal_codes(self):
        self.assertEqual(journal_code("Bill Pmt -Check"), "CD")
        self.assertEqual(journal_code("Invoice"), "SJ")
        self.assertEqual(journal_code("Deposit"), "CR")
        self.assertEqual(journal_code("Something Else"), "GJ")


class ChartBuilderTests(unittest.TestCase):
    def build(self, batch, **kwargs):
        return ChartBuilder(MappingOptions(**kwargs)).build(batch)

    def test_quickbooks_numbers_are_kept(self):
        accounts = self.build(read(sample("account_listing.csv")))
        by_name = {a.source_name: a for a in accounts}
        self.assertEqual(by_name["Checking"].drake_number, "1010")
        self.assertEqual(by_name["Consulting Income"].drake_number, "4000")

    def test_renumbering_uses_the_type_ranges(self):
        accounts = self.build(read(sample("account_listing.csv")),
                              keep_source_numbers=False)
        by_name = {a.source_name: a for a in accounts}
        self.assertTrue(by_name["Checking"].drake_number.startswith("1"))
        self.assertTrue(by_name["Consulting Income"].drake_number.startswith("4"))

    def test_numbers_are_unique_and_deterministic(self):
        first = self.build(read(sample("general_ledger.csv")))
        second = self.build(read(sample("general_ledger.csv")))
        numbers = [a.drake_number for a in first]
        self.assertEqual(len(numbers), len(set(numbers)))
        self.assertEqual(numbers, [a.drake_number for a in second])

    def test_duplicate_source_numbers_fall_back_to_auto_assignment(self):
        batch = Batch(accounts=[
            Account(source_name="Checking", qb_type="BANK", number="1000"),
            Account(source_name="Savings", qb_type="BANK", number="1000"),
        ])
        accounts = self.build(batch)
        numbers = [a.drake_number for a in accounts]
        self.assertEqual(len(set(numbers)), 2)
        self.assertIn("1000", numbers)

    def test_missing_parent_accounts_are_created(self):
        batch = Batch(accounts=[
            Account(source_name="Utilities:Electric:Summer", qb_type="EXP"),
        ])
        names = {a.source_name for a in self.build(batch)}
        self.assertIn("Utilities", names)
        self.assertIn("Utilities:Electric", names)

    def test_subaccount_inherits_the_parent_classification(self):
        batch = Batch(accounts=[
            Account(source_name="Utilities", qb_type="EXP"),
            Account(source_name="Utilities:Electric"),          # no type in the export
        ])
        by_name = {a.source_name: a for a in self.build(batch)}
        self.assertEqual(by_name["Utilities:Electric"].drake_type, "Expense")

    def test_nesting_is_capped_at_drake_level_four(self):
        batch = Batch(accounts=[Account(source_name="A:B:C:D:E:F", qb_type="EXP")])
        deepest = max(self.build(batch), key=lambda a: a.depth)
        self.assertEqual(deepest.depth, 6)
        self.assertEqual(deepest.level, 4)

    def test_name_based_fallback_for_typeless_accounts(self):
        batch = Batch(accounts=[
            Account(source_name="Accounts Payable"),
            Account(source_name="Rent Expense"),
            Account(source_name="Retained Earnings"),
        ])
        by_name = {a.source_name: a for a in self.build(batch)}
        self.assertEqual(by_name["Accounts Payable"].drake_type, "Liability")
        self.assertEqual(by_name["Rent Expense"].drake_type, "Expense")
        self.assertEqual(by_name["Retained Earnings"].drake_type, "Equity")

    def test_normal_balance_follows_the_classification(self):
        batch = Batch(accounts=[
            Account(source_name="Checking", qb_type="BANK"),
            Account(source_name="Consulting Income", qb_type="INC"),
        ])
        by_name = {a.source_name: a for a in self.build(batch)}
        self.assertEqual(by_name["Checking"].normal_balance, "D")
        self.assertEqual(by_name["Consulting Income"].normal_balance, "C")

    def test_accounts_used_only_by_transactions_are_added(self):
        batch = Batch(transactions=[Transaction(lines=[JournalLine(account="Petty Cash")])])
        self.assertIn("Petty Cash", {a.source_name for a in self.build(batch)})


class AccountMapTests(unittest.TestCase):
    def test_overrides_win_over_everything_else(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "map.csv")
            with open(path, "w", newline="", encoding="utf-8") as handle:
                writer = csv.writer(handle)
                writer.writerow(["quickbooks_account", "quickbooks_type",
                                 "drake_account_number", "drake_account_type",
                                 "drake_description", "division"])
                writer.writerow(["Checking", "Bank", "1001", "Asset",
                                 "Main operating account", "01"])
            options = MappingOptions(overrides=MappingOptions.load_overrides(path))
            accounts = ChartBuilder(options).build(read(sample("account_listing.csv")))
            checking = next(a for a in accounts if a.source_name == "Checking")
            self.assertEqual(checking.drake_number, "1001")
            self.assertEqual(checking.description, "Main operating account")
            self.assertEqual(checking.division, "01")


class ValidationTests(unittest.TestCase):
    def test_clean_input_reports_no_errors(self):
        batch = read(sample("quickbooks_export.iif"))
        accounts = ChartBuilder().build(batch)
        self.assertTrue(validate(batch, accounts).ok)

    def test_out_of_balance_entry_is_an_error(self):
        batch = Batch(transactions=[Transaction(
            date=_dt.date(2025, 1, 1),
            reference="X1",
            lines=[JournalLine(account="Checking", debit=Decimal("100.00")),
                   JournalLine(account="Sales", credit=Decimal("90.00"))],
        )])
        report = validate(batch, ChartBuilder().build(batch))
        self.assertFalse(report.ok)
        self.assertTrue(any("do not balance" in e for e in report.errors))
        self.assertTrue(any("10.00" in e for e in report.errors))

    def test_missing_date_is_an_error(self):
        batch = Batch(transactions=[Transaction(
            lines=[JournalLine(account="Checking", debit=Decimal("100.00")),
                   JournalLine(account="Sales", credit=Decimal("100.00"))],
        )])
        report = validate(batch, ChartBuilder().build(batch))
        self.assertTrue(any("no usable date" in e for e in report.errors))

    def test_report_renders_without_blowing_up(self):
        batch = read(sample("journal.csv"))
        text = validate(batch, ChartBuilder().build(batch)).render()
        self.assertIn("Conversion report", text)
        self.assertIn("total debits", text)


class ProfileTests(unittest.TestCase):
    def test_default_profile_is_valid(self):
        profile = Profile.default()
        self.assertEqual([c.field for c in profile.chart_of_accounts.columns][:2],
                         ["level", "number"])

    def test_unknown_field_is_rejected_with_a_helpful_message(self):
        with self.assertRaises(ValueError) as caught:
            Profile.from_dict({
                "chart_of_accounts": {"columns": [{"header": "X", "field": "nope"}]},
                "transactions": {"columns": []},
            })
        self.assertIn("nope", str(caught.exception))

    def test_constant_columns_need_no_field(self):
        profile = Profile.from_dict({
            "chart_of_accounts": {"columns": [{"header": "Co", "constant": "0001"}]},
            "transactions": {"columns": []},
        })
        self.assertEqual(profile.chart_of_accounts.columns[0].constant, "0001")


class EndToEndTests(unittest.TestCase):
    def convert_samples(self, *names, **kwargs):
        tmp = tempfile.mkdtemp()
        result = convert([sample(n) for n in names], tmp, **kwargs)
        return result, read_csv(result.chart_path), read_csv(result.transactions_path)

    def test_iif_round_trip(self):
        result, chart, txns = self.convert_samples("quickbooks_export.iif")
        self.assertTrue(result.report.ok)
        self.assertEqual(chart[0],
                         ["Level", "Account Number", "Account Description",
                          "Account Type", "Normal Balance", "Division"])
        self.assertEqual(len(chart) - 1, 10)
        self.assertEqual(len(txns) - 1, 10)

    def test_debits_equal_credits_in_the_written_file(self):
        _, _, txns = self.convert_samples("quickbooks_export.iif")
        header = txns[0]
        debit, credit = header.index("Debit"), header.index("Credit")
        total_debit = sum(Decimal(r[debit]) for r in txns[1:] if r[debit])
        total_credit = sum(Decimal(r[credit]) for r in txns[1:] if r[credit])
        self.assertEqual(total_debit, total_credit)

    def test_account_listing_plus_ledger_produces_a_typed_chart(self):
        _, chart, txns = self.convert_samples("account_listing.csv", "general_ledger.csv")
        types = {row[3] for row in chart[1:]}
        self.assertNotIn("", types)
        self.assertIn("Asset", types)
        self.assertIn("Income", types)
        # QuickBooks' own numbers carried through to the transaction file.
        self.assertIn("1010", {row[3] for row in txns[1:]})

    def test_entries_come_out_in_date_order(self):
        _, _, txns = self.convert_samples("general_ledger.csv")
        dates = [row[0] for row in txns[1:]]
        self.assertEqual(dates, sorted(dates, key=lambda d: (d[6:], d[:2], d[3:5])))

    def test_journal_codes_are_mapped_from_transaction_type(self):
        _, _, txns = self.convert_samples("journal.csv")
        journals = {row[1] for row in txns[1:]}
        self.assertEqual(journals, {"CD", "SJ", "CR", "GJ"})

    def test_every_transaction_row_carries_an_account_number(self):
        for name in ("quickbooks_export.iif", "journal.csv", "general_ledger.csv",
                     "qbo_journal.csv", "trial_balance.csv"):
            with self.subTest(name=name):
                _, _, txns = self.convert_samples(name)
                self.assertTrue(all(row[3] for row in txns[1:]), name)

    def test_reading_several_files_merges_without_duplicating_accounts(self):
        batch = read_many([sample("account_listing.csv"), sample("account_listing.csv")])
        names = [a.source_name for a in batch.accounts]
        self.assertEqual(len(names), len(set(names)))


if __name__ == "__main__":
    unittest.main()
