"""Classify a source document by filename and, when available, by its text.

Two things come out of classification and both matter:

  doc_type      what the paper is ("W-2", "1099-INT", "K-1 (1120S)")
  wp_section    the workpaper series it files under (100-900)

The doc_type drives which Drake screen the worksheet builds. The section drives
the workpaper index. Filename evidence is weak, so text evidence overrides it.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# Workpaper sections. Fixed so an index reads the same across clients and years.
SECTIONS = {
    100: "Administrative",
    200: "Income",
    300: "Deductions and expenses",
    400: "Balance sheet and trial balance",
    500: "Fixed assets",
    600: "Basis and equity",
    700: "State and local",
    800: "Review",
    900: "Filed return",
}

# (doc_type, wp_section, drake_screen, filename patterns, text patterns)
# drake_screen of None means the document supports a number rather than keying
# into a screen of its own.
RULES: list[tuple[str, int, str | None, list[str], list[str]]] = [
    ("W-2", 200, "W2",
     [r"\bw-?2\b(?!g)"],
     [r"form\s*w-?2\b", r"wage and tax statement"]),
    ("W-2G", 200, "W2G",
     [r"\bw-?2-?g\b"],
     [r"certain gambling winnings"]),
    ("1099-NEC", 200, "99N",
     [r"1099-?nec"],
     [r"1099-?nec", r"nonemployee compensation"]),
    ("1099-MISC", 200, "99M",
     [r"1099-?misc"],
     [r"1099-?misc", r"miscellaneous information"]),
    ("1099-INT", 200, "INT",
     [r"1099-?int"],
     [r"1099-?int", r"interest income"]),
    ("1099-DIV", 200, "DIV",
     [r"1099-?div"],
     [r"1099-?div", r"dividends and distributions"]),
    ("1099-B", 200, "8949",
     [r"1099-?b\b", r"consolidated[ _-]?1099", r"brokerage", r"composite[ _-]?statement"],
     [r"1099-?b\b", r"proceeds from broker"]),
    ("1099-R", 200, "99R",
     [r"1099-?r\b"],
     [r"1099-?r\b", r"distributions from pensions"]),
    ("1099-G", 200, "99G",
     [r"1099-?g\b"],
     [r"1099-?g\b", r"certain government payments"]),
    ("1099-K", 200, "99K",
     [r"1099-?k\b"],
     [r"1099-?k\b", r"payment card and third party network"]),
    ("SSA-1099", 200, "SSA",
     [r"ssa-?1099", r"social[ _-]?security[ _-]?benefit"],
     [r"ssa-?1099", r"social security benefit statement"]),
    ("K-1 (1065)", 200, "K1P",
     [r"k-?1.*1065", r"1065.*k-?1"],
     [r"schedule k-?1\s*\(form 1065\)", r"partner's share of income"]),
    ("K-1 (1120S)", 200, "K1S",
     [r"k-?1.*1120-?s", r"1120-?s.*k-?1"],
     [r"schedule k-?1\s*\(form 1120-?s\)", r"shareholder's share of income"]),
    ("K-1 (1041)", 200, "K1F",
     [r"k-?1.*1041", r"1041.*k-?1"],
     [r"schedule k-?1\s*\(form 1041\)", r"beneficiary's share of income"]),
    ("K-1 (unspecified)", 200, "K1P",
     [r"\bk-?1\b"],
     [r"schedule k-?1"]),
    ("1095-A", 300, "95A",
     [r"1095-?a"],
     [r"1095-?a", r"health insurance marketplace statement"]),
    ("1098-T", 300, "8863",
     [r"1098-?t"],
     [r"1098-?t", r"tuition statement"]),
    ("1098-E", 300, "4",
     [r"1098-?e"],
     [r"1098-?e", r"student loan interest statement"]),
    ("1098 (mortgage interest)", 300, "A",
     [r"1098\b", r"mortgage[ _-]?interest"],
     [r"mortgage interest statement"]),
    ("Charitable contributions", 300, "A",
     [r"charitab", r"donation", r"contribution[ _-]?receipt"],
     [r"charitable contribution", r"no goods or services were provided"]),
    ("Medical expenses", 300, "A",
     [r"medical", r"pharmacy", r"eob\b"],
     [r"explanation of benefits"]),
    ("Property tax", 300, "A",
     [r"property[ _-]?tax", r"real[ _-]?estate[ _-]?tax"],
     [r"real estate tax", r"property tax bill"]),
    ("Childcare receipt", 300, "2441",
     [r"child[ _-]?care", r"daycare", r"2441"],
     [r"dependent care"]),
    ("Estimated tax payments", 100, "ES",
     [r"estimat", r"\b1040-?es\b", r"\bes[ _-]?payment"],
     [r"estimated tax payment", r"form 1040-?es"]),
    ("Business P&L", 300, "C",
     [r"profit[ _-]?and[ _-]?loss", r"\bp&?l\b", r"income[ _-]?statement",
      r"schedule[ _-]?c"],
     [r"profit and loss", r"income statement"]),
    ("Rental statement", 300, "E",
     [r"rental", r"schedule[ _-]?e", r"property[ _-]?statement"],
     [r"rental income", r"property management statement"]),
    ("Depreciation schedule", 500, "4562",
     [r"deprec", r"fixed[ _-]?asset", r"4562", r"asset[ _-]?list"],
     [r"depreciation schedule", r"accumulated depreciation"]),
    ("Asset disposition", 500, "4797",
     [r"4797", r"bill[ _-]?of[ _-]?sale", r"buyer'?s?[ _-]?order", r"disposition", r"\bdeed\b"],
     [r"bill of sale", r"buyer's order"]),
    ("Form 7203 / basis", 600, None,
     [r"7203", r"\bbasis\b", r"capital[ _-]?account", r"\baaa\b"],
     [r"form 7203", r"shareholder stock and debt basis"]),
    ("Loan document", 600, None,
     [r"promissory", r"loan[ _-]?agreement", r"shareholder[ _-]?loan"],
     [r"promissory note"]),
    ("Trial balance / GL", 400, None,
     [r"trial[ _-]?balance", r"\btb\b", r"general[ _-]?ledger", r"\bgl\b",
      r"quickbooks", r"balance[ _-]?sheet"],
     [r"trial balance", r"general ledger"]),
    ("Bank statement", 400, None,
     [r"bank[ _-]?statement", r"\bstatement\b", r"reconcil"],
     [r"beginning balance", r"ending balance"]),
    ("State return / notice", 700, None,
     [r"\bstate\b", r"apportion", r"\bnotice\b", r"department of revenue"],
     [r"department of revenue"]),
    ("Prior-year return", 100, None,
     [r"prior[ _-]?year", r"as[ _-]?filed", r"20\d\d.*return"],
     [r"u\.s\. individual income tax return"]),
    ("Engagement letter", 100, None,
     [r"engagement", r"7216", r"consent"],
     [r"engagement letter"]),
    ("E-file authorization", 100, None,
     [r"8879", r"e-?file", r"efile"],
     [r"form 8879", r"e-file signature authorization"]),
    ("Identification", 100, "PIN",
     [r"driver'?s?[ _-]?licen", r"\bid\b", r"passport"],
     [r"driver license", r"identification card"]),
    ("Organizer", 100, None,
     [r"organizer", r"questionnaire", r"intake"],
     [r"tax organizer"]),
]

SKIP_EXT = {".exe", ".dll", ".msi", ".tmp", ".lnk", ".ini", ".sys", ".db"}
SKIP_NAMES = {".ds_store", "thumbs.db", "desktop.ini"}


@dataclass
class Verdict:
    doc_type: str
    wp_section: int
    drake_screen: str | None
    confidence: str  # "text", "filename", "none"
    evidence: str


def classify(filename: str, text: str = "") -> Verdict:
    """Text evidence wins over filename evidence. Neither means it needs a human."""
    low_text = (text or "").lower()[:20000]
    if low_text:
        for doc_type, section, screen, _fn_pats, txt_pats in RULES:
            for pat in txt_pats:
                m = re.search(pat, low_text)
                if m:
                    return Verdict(doc_type, section, screen, "text",
                                   f"text matched /{pat}/")

    low_name = filename.lower()
    for doc_type, section, screen, fn_pats, _txt_pats in RULES:
        for pat in fn_pats:
            if re.search(pat, low_name):
                return Verdict(doc_type, section, screen, "filename",
                               f"filename matched /{pat}/")

    return Verdict("Unidentified", 800, None, "none", "no pattern matched")


def should_skip(filename: str) -> bool:
    low = filename.lower()
    if low in SKIP_NAMES or low.startswith("~$") or low.startswith("."):
        return True
    return any(low.endswith(ext) for ext in SKIP_EXT)


# Documents expected by form type. Absence is a finding, so this list is the
# point of the intake step rather than a nicety.
EXPECTED = {
    "1040": [
        ("Prior-year return", ["Prior-year return"]),
        ("Engagement letter", ["Engagement letter"]),
        ("W-2s", ["W-2"]),
        ("Interest / dividend 1099s", ["1099-INT", "1099-DIV"]),
        ("Brokerage 1099-B", ["1099-B"]),
        ("K-1s received", ["K-1 (1065)", "K-1 (1120S)", "K-1 (1041)", "K-1 (unspecified)"]),
        ("Form 1095-A (if marketplace coverage)", ["1095-A"]),
        ("Estimated tax payment record", ["Estimated tax payments"]),
        ("E-file authorization (8879)", ["E-file authorization"]),
    ],
    "1120S": [
        ("Prior-year return", ["Prior-year return"]),
        ("Engagement letter", ["Engagement letter"]),
        ("Trial balance or general ledger", ["Trial balance / GL"]),
        ("Bank statements", ["Bank statement"]),
        ("Depreciation schedule", ["Depreciation schedule"]),
        ("Form 7203 / shareholder basis", ["Form 7203 / basis"]),
        ("Officer W-2", ["W-2"]),
        ("Shareholder loan documents", ["Loan document"]),
    ],
    "1065": [
        ("Prior-year return", ["Prior-year return"]),
        ("Engagement letter", ["Engagement letter"]),
        ("Trial balance or general ledger", ["Trial balance / GL"]),
        ("Bank statements", ["Bank statement"]),
        ("Depreciation schedule", ["Depreciation schedule"]),
        ("Partner capital account rollforward", ["Form 7203 / basis"]),
    ],
}


def gaps(form: str, present_types: set[str]) -> list[str]:
    """Expected documents with nothing in the folder that could be them."""
    out = []
    for label, types in EXPECTED.get(form.upper(), []):
        if not present_types.intersection(types):
            out.append(label)
    return out
