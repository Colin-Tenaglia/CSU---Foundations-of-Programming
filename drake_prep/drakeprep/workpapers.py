"""Workpaper index, gaps list, tie-out shell, and open items.

The governing standard: a reader picks up any number on the return and reaches its
source document in one step. The index is what makes that true.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from .classify import SECTIONS, gaps as compute_gaps
from .config import Client, Vault, write_private
from .intake import Document
from .screens import ScreenMap
from .security import mask_text
from .values import Entry, Issue
from .worksheet import TOTAL_FIELDS


def build_index(client: Client, documents: list[Document]) -> str:
    lines = [
        f"## Workpaper index — {client.name} · {client.form} · TY{client.year}",
        "",
        f"Built {date.today().isoformat()} from {len(documents)} documents.",
        "",
    ]

    current = None
    for doc in sorted(documents, key=lambda d: d.ref):
        if doc.wp_section != current:
            current = doc.wp_section
            lines += ["", f"### {current} — {SECTIONS[current]}", "",
                      "| Ref | Document | Type | Modified | Drake screen | Flag |",
                      "|---|---|---|---|---|---|"]
        lines.append(
            f"| {doc.ref} | {mask_text(doc.original_name)} | {doc.doc_type} | "
            f"{doc.modified} | {doc.drake_screen or '—'} | {doc.flag} |"
        )

    lines += [
        "",
        "Flags: **OCR** no readable text, values cannot be extracted · "
        "**CLASSIFY** type not identified · **CHECK** identified from the filename "
        "only, not from the document text.",
        "",
    ]

    missing = compute_gaps(client.form, {d.doc_type for d in documents})
    lines += ["### Not in the file", ""]
    if missing:
        lines.append("Every item below is expected for this return type and nothing "
                     "in the folder matches it. Obtain or document why it does not apply.")
        lines.append("")
        for m in missing:
            lines.append(f"- **{m}**")
    else:
        lines.append("Nothing expected for this return type is obviously absent. "
                     "Absence is judged by document type, so a document filed under an "
                     "unexpected type will not show here.")
    lines.append("")
    return "\n".join(lines)


def build_tie_out(client: Client, smap: ScreenMap, entries: list[Entry]) -> str:
    """A tie-out shell. Per-return amounts are filled in after Drake is keyed."""
    lines = [
        f"## Tie-out — {client.form} TY{client.year}",
        "",
        "One row per material item. Fill **Per return** from Drake after keying, then "
        "the **Diff** column. A difference of zero stays in — it is the evidence the "
        "line was checked.",
        "",
        "| Item | Per source | WP ref | Per return | Diff | Note |",
        "|---|---:|---|---:|---:|---|",
    ]

    from .values import parse_money
    for code, fid, label in TOTAL_FIELDS:
        total = 0.0
        refs: list[str] = []
        found = False
        for e in entries:
            if e.screen.upper() != code:
                continue
            amount = parse_money(e.values.get(fid, ""))
            if amount is None:
                continue
            found = True
            total += float(amount)
            if e.wp_ref:
                refs.append(str(e.wp_ref))
        if found:
            ref_text = ", ".join(refs[:6]) + ("…" if len(refs) > 6 else "")
            lines.append(f"| {label} | {total:,.2f} | {ref_text or '—'} |  |  |  |")

    if len(lines) == 7:
        lines.append("| *no extracted values yet* |  |  |  |  |  |")

    lines += [
        "",
        "Conventions: parentheses for negatives, bold every difference including the "
        "zeros, and the Note column carries the disposition rather than restating the "
        "number.",
        "",
    ]
    return "\n".join(lines)


def build_open_items(client: Client, documents: list[Document],
                     issues: list[Issue]) -> str:
    """What has to be answered before the return can be keyed or signed."""
    blockers = [i for i in issues if i.severity == "blocker"]
    checks = [i for i in issues if i.severity == "check"]
    notes = [i for i in issues if i.severity == "note"]
    needs_ocr = [d for d in documents if d.needs_ocr]
    unclassified = [d for d in documents if d.confidence == "none"]
    missing = compute_gaps(client.form, {d.doc_type for d in documents})

    lines = [
        f"# Open items — {client.name} · {client.form} · TY{client.year}",
        "",
        f"{len(blockers)} blockers, {len(checks)} to check, "
        f"{len(missing)} expected documents not in the file.",
        "",
    ]

    lines += ["## 1. Documents to obtain", ""]
    if missing:
        for m in missing:
            lines.append(f"- [ ] **{m}** — not in the file. Obtain, or record why it "
                         "does not apply.")
    else:
        lines.append("- Nothing expected is obviously absent.")
    lines.append("")

    lines += ["## 2. Documents that cannot be read", ""]
    if needs_ocr:
        lines.append("No text could be extracted from these. Values cannot come off "
                     "them automatically — key by hand or install OCR "
                     "(`ocrmypdf`, `tesseract`) and rerun intake.")
        lines.append("")
        for d in needs_ocr:
            lines.append(f"- [ ] WP {d.ref} — {mask_text(d.original_name)} "
                         f"({d.extract_note or 'no text'})")
    else:
        lines.append("- Every document yielded text.")
    lines.append("")

    lines += ["## 3. Documents not identified", ""]
    if unclassified:
        for d in unclassified:
            lines.append(f"- [ ] WP {d.ref} — {mask_text(d.original_name)} — "
                         "set the type by hand, or add a pattern in `classify.py`.")
    else:
        lines.append("- Every document was identified.")
    lines.append("")

    lines += ["## 4. Blockers", ""]
    if blockers:
        lines.append("Each one stops the return. Resolve before keying.")
        lines.append("")
        for i in blockers:
            lines.append(f"- [ ] {i.line()}")
    else:
        lines.append("- None.")
    lines.append("")

    lines += ["## 5. To check", ""]
    if checks:
        for i in checks:
            lines.append(f"- [ ] {i.line()}")
    else:
        lines.append("- None.")
    lines.append("")

    if notes:
        lines += ["## 6. Noted", ""]
        for i in notes:
            lines.append(f"- {i.line()}")
        lines.append("")

    lines += [
        "---",
        "",
        "**Scope.** This list comes from the documents staged into the vault and the "
        "arithmetic on their face. It does not verify that the amounts on those "
        "documents are correct, does not reach prior-year carryovers or basis history, "
        "and does not check the return as keyed into Drake. Values read from scanned "
        "documents carry OCR risk and every one of them needs a human read against the "
        "paper.",
        "",
    ]
    return "\n".join(lines)


def write_workpapers(vault: Vault, client: Client, documents: list[Document],
                     smap: ScreenMap, entries: list[Entry],
                     issues: list[Issue]) -> dict[str, Path]:
    work = vault.sub(client.slug, "work")
    out = vault.sub(client.slug, "out")
    return {
        "index": write_private(work / "workpaper_index.md",
                               build_index(client, documents)),
        "tie_out": write_private(work / "tie_out.md",
                                 build_tie_out(client, smap, entries)),
        "open_items": write_private(out / "open_items.md",
                                    build_open_items(client, documents, issues)),
    }
