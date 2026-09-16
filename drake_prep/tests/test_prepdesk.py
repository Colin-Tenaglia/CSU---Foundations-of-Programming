"""Tests for the prep desk. Run: python3 -m unittest discover -s tests -v"""

import json
import socket
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from drakeprep import security
from drakeprep.classify import classify, gaps, should_skip
from drakeprep.config import Vault, slugify
from drakeprep.intake import run_intake, load_documents
from drakeprep.packet import build as build_packet
from drakeprep.screens import load_map
from drakeprep.values import (Entry, blank_entries, cross_check, merge_issues,
                              parse_date, parse_money, validate)
from drakeprep.workpapers import build_index, build_open_items
from drakeprep.worksheet import render


class TestMasking(unittest.TestCase):
    def test_ssn_masked(self):
        self.assertEqual(security.mask_text("SSN 412-55-9087"), "SSN ***-**-9087")

    def test_ein_masked(self):
        self.assertEqual(security.mask_text("EIN 84-1120931"), "EIN **-***0931")

    def test_bare_nine_digits_masked(self):
        self.assertIn("***-**-9087", security.mask_text("ssn 412559087 on file"))

    def test_money_not_masked(self):
        text = "Wages 84,200.00 and withholding 9,140.00"
        self.assertEqual(security.mask_text(text), text)

    def test_mask_value_by_type(self):
        self.assertEqual(security.mask_value("412-55-9087", "ssn"), "***-**-9087")
        self.assertEqual(security.mask_value("84-1120931", "ein"), "**-***0931")
        self.assertEqual(security.mask_value("84200.00", "money"), "84200.00")


class TestOfflineGuard(unittest.TestCase):
    def test_connect_blocked(self):
        security.enforce_offline()
        self.addCleanup(setattr, security, "_ALLOW_NETWORK", False)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            with self.assertRaises(security.NetworkBlocked):
                s.connect(("192.0.2.1", 80))


class TestClassification(unittest.TestCase):
    def test_text_beats_filename(self):
        v = classify("scan_001.pdf", "Form W-2 Wage and Tax Statement")
        self.assertEqual(v.doc_type, "W-2")
        self.assertEqual(v.confidence, "text")
        self.assertEqual(v.drake_screen, "W2")

    def test_filename_fallback(self):
        v = classify("1099-INT chase.pdf")
        self.assertEqual(v.doc_type, "1099-INT")
        self.assertEqual(v.confidence, "filename")

    def test_w2g_not_w2(self):
        self.assertEqual(classify("W-2G casino.pdf").doc_type, "W-2G")

    def test_unknown_goes_to_review(self):
        v = classify("misc.pdf")
        self.assertEqual(v.wp_section, 800)
        self.assertEqual(v.confidence, "none")

    def test_k1_flavours(self):
        self.assertEqual(classify("k-1 1120s acme.pdf").doc_type, "K-1 (1120S)")
        self.assertEqual(classify("k-1 1065 acme.pdf").doc_type, "K-1 (1065)")

    def test_skip_junk(self):
        self.assertTrue(should_skip(".DS_Store"))
        self.assertTrue(should_skip("~$draft.docx"))
        self.assertFalse(should_skip("W2.pdf"))

    def test_gaps_reports_absent(self):
        missing = gaps("1040", {"W-2"})
        self.assertIn("K-1s received", missing)
        self.assertNotIn("W-2s", missing)


class TestParsing(unittest.TestCase):
    def test_money_forms(self):
        self.assertEqual(str(parse_money("$1,234.56")), "1234.56")
        self.assertEqual(str(parse_money("(500)")), "-500")
        self.assertIsNone(parse_money(""))
        self.assertIsNone(parse_money("n/a"))

    def test_dates(self):
        self.assertEqual(parse_date("11/14/2025").isoformat(), "2025-11-14")
        self.assertEqual(parse_date("2025-11-14").isoformat(), "2025-11-14")
        self.assertIsNone(parse_date("sometime in fall"))


class TestScreenMaps(unittest.TestCase):
    def test_all_forms_load(self):
        for form in ("1040", "1120S", "1065"):
            smap = load_map(form)
            self.assertTrue(smap.screens, f"{form} has no screens")

    def test_field_ids_unique_within_screen(self):
        for form in ("1040", "1120S", "1065"):
            for screen in load_map(form).screens:
                ids = [f.id for f in screen.fields]
                self.assertEqual(len(ids), len(set(ids)),
                                 f"{form}/{screen.code} has duplicate field ids")

    def test_screen_codes_unique(self):
        for form in ("1040", "1120S", "1065"):
            codes = [s.code for s in load_map(form).screens]
            self.assertEqual(len(codes), len(set(codes)), f"{form} duplicate codes")

    def test_doc_types_resolve_to_a_screen(self):
        """Every doc_type a screen claims must be one classify.py can produce."""
        from drakeprep.classify import RULES
        known = {r[0] for r in RULES}
        for form in ("1040", "1120S", "1065"):
            for screen in load_map(form).screens:
                for dt in screen.doc_types:
                    self.assertIn(dt, known,
                                  f"{form}/{screen.code} claims unknown doc_type {dt!r}")

    def test_maps_ship_unverified(self):
        """They must not claim verification nobody performed."""
        for form in ("1040", "1120S", "1065"):
            self.assertFalse(load_map(form).verified)


class TestValidation(unittest.TestCase):
    def setUp(self):
        self.smap = load_map("1040")

    def test_bad_money_is_a_blocker(self):
        e = Entry(screen="W2", values={"wages": "eighty thousand"})
        issues = validate(self.smap, [e])
        self.assertTrue(any(i.field_id == "wages" and i.severity == "blocker"
                            for i in issues))

    def test_identifier_is_a_check_not_a_blocker(self):
        e = Entry(screen="W2", values={"wages": "1000"})
        issues = validate(self.smap, [e])
        ssn = [i for i in issues if i.field_id == "employee_ssn"]
        self.assertEqual(len(ssn), 1)
        self.assertEqual(ssn[0].severity, "check")

    def test_unknown_field_flagged(self):
        e = Entry(screen="W2", values={"wages": "1000", "nonsense": "x"})
        self.assertTrue(any(i.field_id == "nonsense" for i in validate(self.smap, [e])))

    def test_unknown_screen_flagged(self):
        issues = validate(self.smap, [Entry(screen="NOPE")])
        self.assertEqual(issues[0].severity, "blocker")


class TestArithmeticChecks(unittest.TestCase):
    def setUp(self):
        self.smap = load_map("1040")
        self.limits = self.smap.limits

    def _check(self, entry):
        return cross_check(self.smap, [entry], self.limits)

    def test_correct_w2_is_silent(self):
        e = Entry(screen="W2", values={
            "wages": "84200.00", "ss_wages": "88700.00", "ss_withheld": "5499.40",
            "medicare_wages": "88700.00", "medicare_withheld": "1286.15"})
        self.assertEqual(self._check(e), [])

    def test_ss_withholding_break_caught(self):
        e = Entry(screen="W2", values={"ss_wages": "50000.00", "ss_withheld": "2200.00"})
        self.assertTrue(any(i.field_id == "ss_withheld" for i in self._check(e)))

    def test_wage_base_exceeded(self):
        base = self.limits["ss_wage_base"]
        e = Entry(screen="W2", values={"ss_wages": str(base + 5000),
                                       "ss_withheld": str(round((base + 5000) * 0.062, 2))})
        self.assertTrue(any(i.field_id == "ss_wages" for i in self._check(e)))

    def test_qualified_exceeds_ordinary(self):
        e = Entry(screen="DIV", values={"ordinary_dividends": "100",
                                        "qualified_dividends": "200"})
        issues = self._check(e)
        self.assertEqual(issues[0].severity, "blocker")

    def test_1099r_taxable_over_gross(self):
        e = Entry(screen="99R", values={"gross_distribution": "1000",
                                        "taxable_amount": "1200"})
        self.assertTrue(any(i.severity == "blocker" for i in self._check(e)))

    def test_early_distribution_flagged(self):
        e = Entry(screen="99R", values={"gross_distribution": "1000",
                                        "distribution_code": "1"})
        self.assertTrue(any("72(t)" in i.message for i in self._check(e)))

    def test_holding_period_vs_box(self):
        e = Entry(screen="8949", values={"date_acquired": "06/01/2025",
                                         "date_sold": "11/14/2025",
                                         "form8949_box": "D"})
        self.assertTrue(any(i.field_id == "form8949_box" for i in self._check(e)))

    def test_sold_before_acquired(self):
        e = Entry(screen="8949", values={"date_acquired": "11/14/2025",
                                         "date_sold": "06/01/2025"})
        self.assertTrue(any(i.severity == "blocker" for i in self._check(e)))

    def test_s_corp_loss_without_7203(self):
        e = Entry(screen="K1S", values={"ordinary_income": "-18400"})
        self.assertTrue(any("1366(d)" in i.message for i in self._check(e)))

    def test_1099nec_exceeds_schedule_c_receipts(self):
        entries = [
            Entry(screen="99N", values={"nonemployee_comp": "40000",
                                        "schedule_c_link": "Redline"}),
            Entry(screen="C", values={"business_name": "Redline",
                                      "gross_receipts": "30000"}),
        ]
        issues = cross_check(self.smap, entries, self.limits)
        self.assertTrue(any(i.screen == "C" and i.severity == "blocker" for i in issues))

    def test_slcsp_zero_with_advance_credit(self):
        e = Entry(screen="95A", values={"monthly_detail_keyed": "X",
                                        "annual_slcsp": "0",
                                        "annual_advance_ptc": "4200"})
        self.assertTrue(any(i.field_id == "annual_slcsp" for i in self._check(e)))


class TestMergeIssues(unittest.TestCase):
    def test_specific_finding_wins_over_generic(self):
        smap = load_map("1040")
        entries = [Entry(screen="K1S", values={"ordinary_income": "-1000"})]
        issues = merge_issues(validate(smap, entries), cross_check(smap, entries, {}))
        f7203 = [i for i in issues if i.field_id == "form_7203_in_file"]
        self.assertEqual(len(f7203), 1)
        self.assertIn("1366(d)", f7203[0].message)

    def test_blockers_sort_first(self):
        smap = load_map("1040")
        entries = [Entry(screen="W2", values={"wages": "not a number"})]
        issues = merge_issues(validate(smap, entries), cross_check(smap, entries, {}))
        self.assertEqual(issues[0].severity, "blocker")


class TestEndToEnd(unittest.TestCase):
    """Intake a folder, build everything, confirm the source folder is untouched."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.source = root / "client docs"
        self.source.mkdir()
        (self.source / "W2 acme.txt").write_text(
            "Form W-2 Wage and Tax Statement\n"
            "b Employer identification number 84-1120931\n"
            "a social security number 412-55-9087\n"
            "1 Wages, tips, other compensation 84,200.00\n")
        (self.source / "1099-INT bank.txt").write_text(
            "Form 1099-INT Interest Income\n1 Interest income 1,842.19\n")
        (self.source / "engagement letter.txt").write_text("Engagement letter\n")
        (self.source / ".DS_Store").write_text("junk")
        self.before = sorted(p.name for p in self.source.iterdir())

        self.vault = Vault(root / "vault")
        self.vault.init()
        self.client = self.vault.add_client("Smith, John", 2025, "1040")
        self.documents = run_intake(self.vault, self.client, self.source)

    def test_source_folder_untouched(self):
        self.assertEqual(sorted(p.name for p in self.source.iterdir()), self.before)

    def test_junk_skipped(self):
        self.assertEqual(len(self.documents), 3)

    def test_refs_are_sectioned(self):
        by_type = {d.doc_type: d for d in self.documents}
        self.assertTrue(200 <= by_type["W-2"].ref < 300)
        self.assertTrue(100 <= by_type["Engagement letter"].ref < 200)

    def test_documents_reload(self):
        again = load_documents(self.vault, self.client)
        self.assertEqual([d.ref for d in again], [d.ref for d in self.documents])

    def test_staged_copies_exist_and_are_private(self):
        for d in self.documents:
            staged = self.vault.sub(self.client.slug, "docs") / d.staged_name
            self.assertTrue(staged.exists())
            self.assertEqual(staged.stat().st_mode & 0o777, 0o600)

    def test_intake_is_deterministic(self):
        again = run_intake(self.vault, self.client, self.source)
        self.assertEqual([(d.ref, d.doc_type) for d in again],
                         [(d.ref, d.doc_type) for d in self.documents])

    def test_packet_masks_identifiers(self):
        smap = load_map("1040")
        build_packet(self.vault, self.client, self.documents, smap)
        pdir = self.vault.sub(self.client.slug, "packet")
        blob = "\n".join(p.read_text() for p in (pdir / "documents").glob("*.txt"))
        self.assertNotIn("412-55-9087", blob)
        self.assertNotIn("84-1120931", blob)
        self.assertIn("84,200.00", blob)

    def test_packet_schema_is_valid_json(self):
        smap = load_map("1040")
        build_packet(self.vault, self.client, self.documents, smap)
        schema = json.loads(
            (self.vault.sub(self.client.slug, "packet") / "schema.json").read_text())
        self.assertEqual(schema["form"], "1040")
        self.assertTrue(schema["screens"])

    def test_index_lists_gaps(self):
        text = build_index(self.client, self.documents)
        self.assertIn("Not in the file", text)
        self.assertIn("K-1s received", text)

    def test_blank_worksheet_renders_every_screen(self):
        smap = load_map("1040")
        entries = blank_entries(smap, self.documents)
        text = render(self.client, smap, entries)
        for code in ("W2", "INT", "8949", "ES"):
            self.assertIn(f"Screen `{code}`", text)
        self.assertIn("UNVERIFIED", text)

    def test_keying_sheet_hides_empty_screens(self):
        smap = load_map("1040")
        entries = [Entry(screen="W2", wp_ref=200, values={"wages": "84200.00"})]
        text = render(self.client, smap, entries, filled_only=True)
        self.assertIn("Screen `W2`", text)
        self.assertNotIn("Screen `8863`", text)

    def test_open_items_states_its_scope(self):
        text = build_open_items(self.client, self.documents, [])
        self.assertIn("**Scope.**", text)
        self.assertIn("OCR risk", text)


class TestConfig(unittest.TestCase):
    def test_slugify(self):
        self.assertEqual(slugify("Smith, John & Mary"), "smith-john-mary")

    def test_bad_form_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Vault(Path(tmp) / "v")
            vault.init()
            with self.assertRaises(ValueError):
                vault.add_client("X", 2025, "1120C")


if __name__ == "__main__":
    unittest.main()
