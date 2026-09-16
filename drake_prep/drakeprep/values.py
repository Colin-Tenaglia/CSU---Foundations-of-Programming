"""Extracted values, their validation, and the arithmetic checks over them.

A value in here is a proposed Drake entry. It carries the workpaper ref it came
from, so the preparer can go from the keying sheet back to the paper in one step.
That round trip is the whole point of the desk.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict, field
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

from .config import Client, Vault, write_private
from .screens import ScreenMap, Screen

CONFIDENCE = ("high", "medium", "low", "unread")

# Masked out of the packet, so a model never proposes them. A preparer
# keys these from the paper.
BY_HAND_TYPES = {"ssn", "ein", "account"}


@dataclass
class Entry:
    """One Drake screen instance, filled from one source document."""
    screen: str
    instance: int = 1
    wp_ref: int | None = None
    source_doc: str = ""
    values: dict[str, str] = field(default_factory=dict)
    confidence: dict[str, str] = field(default_factory=dict)
    notes: str = ""

    def key(self) -> tuple[str, int]:
        return (self.screen.upper(), self.instance)


@dataclass
class Issue:
    severity: str        # blocker | check | note
    screen: str
    instance: int
    field_id: str
    message: str
    wp_ref: int | None = None

    def line(self) -> str:
        ref = f" [WP {self.wp_ref}]" if self.wp_ref else ""
        where = f"{self.screen}#{self.instance}"
        fld = f".{self.field_id}" if self.field_id else ""
        return f"{self.severity.upper():<8} {where}{fld}{ref} — {self.message}"


# ---------------------------------------------------------------- parsing

_MONEY_CLEAN = re.compile(r"[,$\s]")


def parse_money(raw: str) -> Decimal | None:
    """'$1,234.56' -> Decimal('1234.56'). '(500)' -> Decimal('-500')."""
    if raw is None:
        return None
    s = str(raw).strip()
    if not s:
        return None
    neg = s.startswith("(") and s.endswith(")")
    s = s.strip("()")
    s = _MONEY_CLEAN.sub("", s)
    if not s:
        return None
    try:
        val = Decimal(s)
    except InvalidOperation:
        return None
    return -val if neg else val


DATE_FORMATS = ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y", "%m-%d-%Y", "%Y%m%d", "%b %d, %Y")


def parse_date(raw: str) -> date | None:
    if not raw:
        return None
    s = str(raw).strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def is_truthy(raw: str) -> bool:
    return str(raw).strip().lower() in {"x", "y", "yes", "true", "1", "checked"}


# ---------------------------------------------------------------- storage

def values_path(vault: Vault, client: Client) -> Path:
    return vault.sub(client.slug, "out") / "values.json"


def load_entries(vault: Vault, client: Client) -> list[Entry]:
    path = values_path(vault, client)
    if not path.exists():
        return []
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [Entry(**e) for e in raw.get("entries", [])]


def save_entries(vault: Vault, client: Client, entries: list[Entry]) -> Path:
    payload = {
        "client": client.slug,
        "form": client.form,
        "tax_year": client.year,
        "updated": datetime.now().isoformat(timespec="seconds"),
        "_warning": "Contains unmasked taxpayer identifiers. Owner-read only. "
                    "Never goes into a packet and never leaves the vault.",
        "entries": [asdict(e) for e in entries],
    }
    return write_private(values_path(vault, client),
                         json.dumps(payload, indent=2, default=str))


def blank_entries(smap: ScreenMap, documents) -> list[Entry]:
    """One entry per document that maps to a screen, plus one per single-instance
    screen that has no document behind it. Gives the preparer a full skeleton."""
    entries: list[Entry] = []
    counts: dict[str, int] = {}
    for doc in sorted(documents, key=lambda d: d.ref):
        if not doc.drake_screen:
            continue
        screen = smap.by_code(doc.drake_screen)
        if screen is None:
            continue
        n = counts.get(screen.code, 0) + 1
        counts[screen.code] = n
        entries.append(Entry(screen=screen.code, instance=n if screen.multi else 1,
                             wp_ref=doc.ref, source_doc=doc.staged_name))
    for screen in smap.screens:
        if screen.code not in counts and not screen.multi:
            entries.append(Entry(screen=screen.code, instance=1))
    entries.sort(key=lambda e: (_screen_order(smap, e.screen), e.instance))
    return entries


def _screen_order(smap: ScreenMap, code: str) -> int:
    s = smap.by_code(code)
    return s.order if s else 999


# ---------------------------------------------------------------- validation

def validate(smap: ScreenMap, entries: list[Entry]) -> list[Issue]:
    """Type and required-field validation, field by field."""
    issues: list[Issue] = []
    for entry in entries:
        screen = smap.by_code(entry.screen)
        if screen is None:
            issues.append(Issue("blocker", entry.screen, entry.instance, "",
                                f"screen {entry.screen} is not in {smap.path.name}",
                                entry.wp_ref))
            continue
        known = {f.id: f for f in screen.fields}
        for fid in entry.values:
            if fid not in known:
                issues.append(Issue("check", screen.code, entry.instance, fid,
                                    f"field not on screen {screen.code} — typo, or the "
                                    "screen map needs updating", entry.wp_ref))
        for f in screen.fields:
            raw = entry.values.get(f.id, "")
            if not str(raw).strip():
                if f.required and f.type in BY_HAND_TYPES:
                    # Identifiers are masked out of the packet on purpose. Their
                    # absence is expected work, not a defect in the extraction.
                    issues.append(Issue("check", screen.code, entry.instance, f.id,
                                        f"key by hand from the paper — {f.label}",
                                        entry.wp_ref))
                elif f.required:
                    issues.append(Issue("blocker", screen.code, entry.instance, f.id,
                                        f"required and empty — {f.label}", entry.wp_ref))
                continue
            issues.extend(_check_type(screen, entry, f, raw))
    return issues


def _check_type(screen: Screen, entry: Entry, f, raw) -> list[Issue]:
    out: list[Issue] = []
    if f.type == "money":
        if parse_money(raw) is None:
            out.append(Issue("blocker", screen.code, entry.instance, f.id,
                             f"not a number: {raw!r}", entry.wp_ref))
    elif f.type == "date":
        if parse_date(raw) is None:
            out.append(Issue("blocker", screen.code, entry.instance, f.id,
                             f"not a date: {raw!r} (use MM/DD/YYYY)", entry.wp_ref))
    elif f.type in ("ssn", "ein"):
        digits = re.sub(r"\D", "", str(raw))
        if len(digits) != 9:
            out.append(Issue("blocker", screen.code, entry.instance, f.id,
                             f"{f.type.upper()} must be 9 digits, got {len(digits)}",
                             entry.wp_ref))
    elif f.type == "percent":
        if parse_money(str(raw).rstrip("%")) is None:
            out.append(Issue("check", screen.code, entry.instance, f.id,
                             f"not a percentage: {raw!r}", entry.wp_ref))
    elif f.type == "int":
        if not re.fullmatch(r"-?\d+", str(raw).strip()):
            out.append(Issue("check", screen.code, entry.instance, f.id,
                             f"not a whole number: {raw!r}", entry.wp_ref))
    elif f.type == "state":
        if not re.fullmatch(r"[A-Za-z]{2}", str(raw).strip()):
            out.append(Issue("check", screen.code, entry.instance, f.id,
                             f"state should be a two-letter code, got {raw!r}",
                             entry.wp_ref))
    return out


# ---------------------------------------------------------------- arithmetic

def cross_check(smap: ScreenMap, entries: list[Entry],
                limits: dict | None = None) -> list[Issue]:
    """Arithmetic that the source document should satisfy on its face.

    These catch transcription errors and corrected forms. A break is not proof of
    an error; it is proof that somebody needs to look."""
    limits = limits or {}
    ss_rate = Decimal(str(limits.get("ss_rate", "0.062")))
    mc_rate = Decimal(str(limits.get("medicare_rate", "0.0145")))
    wage_base = parse_money(str(limits.get("ss_wage_base", "")))
    tol = Decimal("2.00")
    issues: list[Issue] = []

    for e in entries:
        v = e.values
        code = e.screen.upper()

        if code == "W2":
            ssw, sst = parse_money(v.get("ss_wages", "")), parse_money(v.get("ss_withheld", ""))
            if ssw is not None and sst is not None and ssw > 0:
                expect = (ssw * ss_rate).quantize(Decimal("0.01"))
                if abs(expect - sst) > tol:
                    issues.append(Issue("check", code, e.instance, "ss_withheld",
                                        f"box 4 is ${sst}; box 3 x {ss_rate} is ${expect}. "
                                        "Corrected W-2, or a keying error.", e.wp_ref))
            mcw, mct = parse_money(v.get("medicare_wages", "")), parse_money(v.get("medicare_withheld", ""))
            if mcw is not None and mct is not None and mcw > 0:
                expect = (mcw * mc_rate).quantize(Decimal("0.01"))
                if mct < expect - tol:
                    issues.append(Issue("check", code, e.instance, "medicare_withheld",
                                        f"box 6 is ${mct}; box 5 x {mc_rate} is ${expect}.",
                                        e.wp_ref))
            if wage_base and ssw is not None and ssw > wage_base:
                issues.append(Issue("check", code, e.instance, "ss_wages",
                                    f"box 3 ${ssw} exceeds the ${wage_base} wage base.",
                                    e.wp_ref))
            wages, mcw = parse_money(v.get("wages", "")), parse_money(v.get("medicare_wages", ""))
            if wages is not None and mcw is not None and mcw < wages:
                issues.append(Issue("note", code, e.instance, "medicare_wages",
                                    f"box 5 ${mcw} is below box 1 ${wages}. Unusual — "
                                    "box 5 normally exceeds box 1 by deferrals.", e.wp_ref))

        elif code == "DIV":
            ordinary = parse_money(v.get("ordinary_dividends", ""))
            qualified = parse_money(v.get("qualified_dividends", ""))
            if ordinary is not None and qualified is not None and qualified > ordinary:
                issues.append(Issue("blocker", code, e.instance, "qualified_dividends",
                                    f"box 1b ${qualified} exceeds box 1a ${ordinary}.",
                                    e.wp_ref))

        elif code == "99R":
            gross = parse_money(v.get("gross_distribution", ""))
            taxable = parse_money(v.get("taxable_amount", ""))
            if gross is not None and taxable is not None and taxable > gross:
                issues.append(Issue("blocker", code, e.instance, "taxable_amount",
                                    f"box 2a ${taxable} exceeds box 1 ${gross}.", e.wp_ref))
            dcode = str(v.get("distribution_code", "")).strip().upper()
            if dcode.startswith("1"):
                issues.append(Issue("check", code, e.instance, "distribution_code",
                                    "code 1 — early distribution. Confirm whether a "
                                    "§72(t) exception applies on Form 5329.", e.wp_ref))
            if dcode.startswith("G") and taxable and taxable > 0:
                issues.append(Issue("check", code, e.instance, "taxable_amount",
                                    "code G is a direct rollover but box 2a is not zero. "
                                    "Confirm it is a Roth conversion.", e.wp_ref))

        elif code == "8949":
            acq, sold = parse_date(v.get("date_acquired", "")), parse_date(v.get("date_sold", ""))
            if acq and sold and sold < acq:
                issues.append(Issue("blocker", code, e.instance, "date_sold",
                                    f"sold {sold} before acquired {acq}.", e.wp_ref))
            box = str(v.get("form8949_box", "")).strip().upper()
            if acq and sold and box:
                long_term = (sold - acq).days > 365
                if long_term and box in {"A", "B", "C"}:
                    issues.append(Issue("check", code, e.instance, "form8949_box",
                                        f"held {(sold - acq).days} days (long term) but "
                                        f"box {box} is a short-term box.", e.wp_ref))
                if not long_term and box in {"D", "E", "F"}:
                    issues.append(Issue("check", code, e.instance, "form8949_box",
                                        f"held {(sold - acq).days} days (short term) but "
                                        f"box {box} is a long-term box.", e.wp_ref))

        elif code == "95A":
            if not is_truthy(v.get("monthly_detail_keyed", "")):
                issues.append(Issue("blocker", code, e.instance, "monthly_detail_keyed",
                                    "monthly rows not confirmed keyed. A missing month "
                                    "understates the advance credit.", e.wp_ref))
            slcsp = parse_money(v.get("annual_slcsp", ""))
            aptc = parse_money(v.get("annual_advance_ptc", ""))
            if slcsp is not None and slcsp == 0 and aptc and aptc > 0:
                issues.append(Issue("blocker", code, e.instance, "annual_slcsp",
                                    "column B is zero with advance credit paid. Look up "
                                    "the SLCSP; do not key zero.", e.wp_ref))

        elif code == "K1S":
            ordinary = parse_money(v.get("ordinary_income", ""))
            if ordinary is not None and ordinary < 0 and not is_truthy(v.get("form_7203_in_file", "")):
                issues.append(Issue("blocker", code, e.instance, "form_7203_in_file",
                                    f"loss of ${ordinary} claimed with no Form 7203 in the "
                                    "file. §1366(d) limits the loss to basis.", e.wp_ref))

        elif code == "C":
            receipts = parse_money(v.get("gross_receipts", ""))
            if receipts is not None and receipts == 0:
                issues.append(Issue("check", code, e.instance, "gross_receipts",
                                    "gross receipts of zero on a filed Schedule C.", e.wp_ref))
            if is_truthy(v.get("required_1099s", "")) and not is_truthy(v.get("filed_1099s", "")):
                issues.append(Issue("check", code, e.instance, "filed_1099s",
                                    "line I says 1099s were required, line J says they were "
                                    "not filed. §6721 penalty exposure.", e.wp_ref))

        elif code == "E":
            frd = v.get("fair_rental_days", "")
            pud = v.get("personal_use_days", "")
            if str(frd).strip() and str(pud).strip():
                try:
                    if int(frd) + int(pud) > 366:
                        issues.append(Issue("check", code, e.instance, "fair_rental_days",
                                            f"fair rental {frd} + personal {pud} exceeds a year.",
                                            e.wp_ref))
                    if int(pud) > 14 and int(pud) > int(frd) * 0.1:
                        issues.append(Issue("check", code, e.instance, "personal_use_days",
                                            "personal use exceeds the §280A(d) threshold — "
                                            "expenses must be allocated and the loss limited.",
                                            e.wp_ref))
                except ValueError:
                    pass

    issues.extend(_schedule_c_receipts(entries))
    return issues


def _schedule_c_receipts(entries: list[Entry]) -> list[Issue]:
    """1099-NEC and 1099-K amounts linked to a Schedule C should be inside its
    gross receipts. Receipts below the forms is the notice that writes itself."""
    reported: dict[str, Decimal] = {}
    for e in entries:
        if e.screen.upper() == "99N":
            link = str(e.values.get("schedule_c_link", "")).strip().lower()
            amt = parse_money(e.values.get("nonemployee_comp", ""))
            if link and amt:
                reported[link] = reported.get(link, Decimal(0)) + amt
    out: list[Issue] = []
    for e in entries:
        if e.screen.upper() != "C":
            continue
        name = str(e.values.get("business_name", "")).strip().lower()
        receipts = parse_money(e.values.get("gross_receipts", ""))
        if name in reported and receipts is not None:
            forms_total = reported[name]
            if receipts < forms_total:
                out.append(Issue("blocker", "C", e.instance, "gross_receipts",
                                 f"gross receipts ${receipts} are below the ${forms_total} "
                                 "of 1099-NEC linked to this business.", e.wp_ref))
    return out


SEVERITY_RANK = {"blocker": 0, "check": 1, "note": 2}


def merge_issues(*groups: list[Issue]) -> list[Issue]:
    """Collapse duplicate findings on the same field.

    A required-and-empty blocker and a specific arithmetic finding on the same
    field are one problem. Keep the specific one — it says what to do.
    """
    best: dict[tuple[str, int, str], Issue] = {}
    loose: list[Issue] = []
    for group in groups:
        for issue in group:
            if not issue.field_id:
                loose.append(issue)
                continue
            key = (issue.screen.upper(), issue.instance, issue.field_id)
            current = best.get(key)
            if current is None:
                best[key] = issue
                continue
            if SEVERITY_RANK[issue.severity] < SEVERITY_RANK[current.severity]:
                best[key] = issue
            elif (issue.severity == current.severity
                  and len(issue.message) > len(current.message)):
                best[key] = issue
    out = list(best.values()) + loose
    out.sort(key=lambda i: (SEVERITY_RANK[i.severity], i.screen, i.instance, i.field_id))
    return out
