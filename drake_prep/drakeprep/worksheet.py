"""Render the Drake-ordered worksheets.

Two documents come out of here and they have different jobs.

  worksheet.md    every field on every screen, in Drake order, with the workpaper
                  ref beside it. This is what gets filled in and reviewed.
  keying_sheet.md only the fields that have a value, same order. This is what sits
                  next to the keyboard while somebody types into Drake.

Both mask identifiers. The unmasked values live in out/values.json and stay there.
"""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

from .config import Client, Vault, write_private
from .screens import ScreenMap, Screen
from .security import mask_value
from .values import Entry, parse_money

MASKED_TYPES = {"ssn", "ein", "account"}


def _cell(value: str, ftype: str) -> str:
    if not str(value).strip():
        return " "
    if ftype in MASKED_TYPES:
        return mask_value(value, ftype)
    if ftype == "money":
        amount = parse_money(value)
        if amount is not None:
            return f"({abs(amount):,.2f})" if amount < 0 else f"{amount:,.2f}"
    if ftype == "checkbox":
        return "X" if str(value).strip().lower() in {"x", "y", "yes", "true", "1"} else " "
    return str(value).replace("|", "\\|")


def _header(client: Client, smap: ScreenMap, title: str) -> list[str]:
    lines = [
        f"# {title} — {client.name}",
        "",
        f"**{client.form} · TY{client.year}** · prepared {date.today().isoformat()}",
        "",
        f"> {smap.status_line}",
        "",
        "> Identifiers are masked. Full values are in `out/values.json`, which stays "
        "in the vault.",
        "",
    ]
    if not smap.verified:
        lines += [
            "> **Do not key from this sheet until the screen map has been walked "
            "against your Drake install.** Field order here follows the IRS form, "
            "which is close to Drake's layout but has not been confirmed.",
            "",
        ]
    return lines


def _screen_block(screen: Screen, entry: Entry | None, instance_label: str,
                  filled_only: bool) -> list[str]:
    values = entry.values if entry else {}
    rows = []
    for f in screen.fields:
        raw = values.get(f.id, "")
        if filled_only and not str(raw).strip():
            continue
        flag = ""
        if entry and entry.confidence.get(f.id) in ("low", "unread"):
            flag = " ⚠"
        elif f.required and not str(raw).strip():
            flag = " ●"
        rows.append((f.display_box, f.label + flag, _cell(raw, f.type), f.note))

    if not rows:
        return []

    ref = ""
    if entry and entry.wp_ref:
        ref = f" · WP {entry.wp_ref}"
        if entry.source_doc:
            ref += f" · `{entry.source_doc}`"

    out = [f"### Screen `{screen.code}` — {screen.title}{instance_label}{ref}", ""]
    if screen.note:
        out += [f"*{screen.note}*", ""]
    out += ["| Box | Field | Value | Note |", "|---|---|---|---|"]
    for box, label, value, note in rows:
        out.append(f"| {box} | {label} | {value} | {note} |")
    out.append("")
    if entry and entry.notes:
        out += [f"**Preparer note:** {entry.notes}", ""]
    return out


def render(client: Client, smap: ScreenMap, entries: list[Entry],
           filled_only: bool = False) -> str:
    title = "Drake keying sheet" if filled_only else "Drake data entry worksheet"
    lines = _header(client, smap, title)
    if not filled_only:
        lines += [
            "Legend: **●** required and empty · **⚠** low confidence, verify against "
            "the source document.",
            "",
        ]

    by_screen: dict[str, list[Entry]] = {}
    for e in entries:
        by_screen.setdefault(e.screen.upper(), []).append(e)

    current_section = None
    for screen in smap.screens:
        screen_entries = sorted(by_screen.get(screen.code.upper(), []),
                                key=lambda e: e.instance)
        if not screen_entries:
            if filled_only:
                continue
            screen_entries = [None]

        section = screen.wp_section
        if section != current_section:
            from .classify import SECTIONS
            lines += [f"## {section} — {SECTIONS.get(section, 'Other')}", ""]
            current_section = section

        for entry in screen_entries:
            label = ""
            if screen.multi and entry:
                label = f" #{entry.instance}"
            elif screen.multi:
                label = " #1"
            block = _screen_block(screen, entry, label, filled_only)
            lines += block

    lines += _totals_block(smap, entries)
    return "\n".join(lines).rstrip() + "\n"


# Fields whose totals a reviewer checks first. Screen code -> (field id, label).
TOTAL_FIELDS = [
    ("W2", "wages", "W-2 wages (box 1)"),
    ("W2", "fed_withheld", "W-2 federal withholding (box 2)"),
    ("INT", "interest_income", "Interest income (box 1)"),
    ("DIV", "ordinary_dividends", "Ordinary dividends (box 1a)"),
    ("DIV", "qualified_dividends", "Qualified dividends (box 1b)"),
    ("99N", "nonemployee_comp", "Nonemployee compensation (box 1)"),
    ("99R", "gross_distribution", "Retirement gross distributions (box 1)"),
    ("99R", "taxable_amount", "Retirement taxable amount (box 2a)"),
    ("SSA", "net_benefits", "Social security net benefits (box 5)"),
    ("8949", "proceeds", "Capital transaction proceeds"),
    ("8949", "cost_basis", "Capital transaction basis"),
    ("C", "gross_receipts", "Schedule C gross receipts"),
    ("E", "rents_received", "Schedule E rents received"),
    ("K1P", "ordinary_income", "K-1 (1065) ordinary income"),
    ("K1S", "ordinary_income", "K-1 (1120S) ordinary income"),
]


def _totals_block(smap: ScreenMap, entries: list[Entry]) -> list[str]:
    """Control totals. The reviewer compares these against the Drake return."""
    sums: dict[tuple[str, str], tuple[str, float, int]] = {}
    for e in entries:
        for code, fid, label in TOTAL_FIELDS:
            if e.screen.upper() != code:
                continue
            amount = parse_money(e.values.get(fid, ""))
            if amount is None:
                continue
            key = (code, fid)
            prev = sums.get(key, (label, 0.0, 0))
            sums[key] = (label, prev[1] + float(amount), prev[2] + 1)

    if not sums:
        return []
    lines = ["## Control totals", "",
             "Compare each against the Drake return before the return is signed.",
             "", "| Item | Documents | Total |", "|---|---:|---:|"]
    for code, fid, label in TOTAL_FIELDS:
        entry = sums.get((code, fid))
        if entry:
            lines.append(f"| {entry[0]} | {entry[2]} | {entry[1]:,.2f} |")
    lines.append("")
    return lines


def write_worksheets(vault: Vault, client: Client, smap: ScreenMap,
                     entries: list[Entry]) -> dict[str, Path]:
    out = vault.sub(client.slug, "out")
    paths = {
        "worksheet": write_private(out / "worksheet.md",
                                   render(client, smap, entries, filled_only=False)),
        "keying_sheet": write_private(out / "keying_sheet.md",
                                      render(client, smap, entries, filled_only=True)),
        "worksheet_csv": _write_csv(out / "worksheet.csv", smap, entries),
    }
    return paths


def _write_csv(path: Path, smap: ScreenMap, entries: list[Entry]) -> Path:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["screen", "instance", "wp_ref", "box", "field_id", "label",
                    "type", "value_masked", "confidence", "required"])
        for e in sorted(entries, key=lambda e: (_order(smap, e.screen), e.instance)):
            screen = smap.by_code(e.screen)
            if screen is None:
                continue
            for f in screen.fields:
                raw = e.values.get(f.id, "")
                w.writerow([screen.code, e.instance, e.wp_ref or "", f.box, f.id,
                            f.label, f.type, _cell(raw, f.type).strip(),
                            e.confidence.get(f.id, ""), "yes" if f.required else ""])
    path.chmod(0o600)
    return path


def _order(smap: ScreenMap, code: str) -> int:
    s = smap.by_code(code)
    return s.order if s else 999
