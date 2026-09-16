"""Build the bundle that gets handed to Claude.

This is the seam that keeps the desk offline. The app writes a packet, the packet
goes to Claude however you like, and Claude's answer comes back as one JSON file
that `prepdesk fill` reads. No key, no API call, no document leaving the machine
unless you carry it.

Document text in the packet is masked by default. An SSN is keyed by a human from
the paper; a model does not need to see it to read box 1 of a W-2.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from .config import Client, Vault, write_private
from .intake import Document
from .screens import ScreenMap
from .security import mask_text

MAX_DOC_CHARS = 24000


def _schema(smap: ScreenMap, screens_used: set[str]) -> dict:
    return {
        "form": smap.form,
        "screen_map": smap.path.name,
        "screens": [
            {
                "code": s.code,
                "title": s.title,
                "multi": s.multi,
                "doc_types": s.doc_types,
                "note": s.note,
                "fields": [
                    {"id": f.id, "box": f.box, "label": f.label, "type": f.type,
                     "required": f.required, "note": f.note}
                    for f in s.fields
                ],
            }
            for s in smap.screens if s.code.upper() in screens_used
        ],
    }


INSTRUCTIONS = """\
# Extraction packet — {label}

You are reading staged tax source documents and proposing Drake data entry values.
You are not preparing a return and not giving tax advice. Read, transcribe, flag.

## What to produce

One JSON file, matching `schema.json` in this packet:

```json
{{
  "entries": [
    {{
      "screen": "W2",
      "instance": 1,
      "wp_ref": 210,
      "source_doc": "210_W2_acme-corp.pdf",
      "values": {{ "employer_name": "Acme Corp", "wages": "84200.00" }},
      "confidence": {{ "wages": "high", "box12a_amount": "low" }},
      "notes": "Box 12 code illegible in the scan."
    }}
  ]
}}
```

## Rules

1. **Only fields in `schema.json`.** Use the exact `id`. A value that has nowhere to
   go belongs in `notes`, not in an invented field.
2. **One entry per source document** for screens marked `multi`. Number `instance`
   from 1 within each screen. Carry the `wp_ref` and `source_doc` through from the
   document heading — that is how a number gets back to its paper.
3. **Transcribe, do not compute.** Amounts go in as they appear, digits only, with a
   decimal point and no currency symbol or thousands separator. Negatives take a
   leading minus sign. A box that is blank on the paper stays out of `values`
   entirely; do not write "0" for a blank box.
4. **Dates as MM/DD/YYYY.** Checkboxes as "X" when checked, omitted when not.
5. **Identifiers are masked in this packet.** SSN, EIN, and account fields read as
   `***-**-1234`. Leave those fields out of `values` — they are keyed by hand from
   the paper.
6. **Mark confidence honestly.** `high` when the number is unambiguous on the page,
   `medium` when the layout made you infer it, `low` when the scan is poor or the
   label is ambiguous, `unread` when you could not find it at all. Every `low` and
   `unread` becomes an open item a preparer has to look at, which is the point. A
   wrong `high` is worse than an honest `low`.
7. **Never invent a number.** If a document is unreadable, return an entry with empty
   `values` and say so in `notes`.
8. **Flag contradictions in `notes`** — a box that does not foot, a corrected form, a
   document that appears to belong to a different taxpayer or year.

## What is here

- `schema.json` — the screens and fields you may fill
- `documents/` — the extracted text, one file per document, named by workpaper ref
- `documents.md` — the index, with each document's type and the screen it maps to

## Return it

Write your JSON to a file and hand it back with:

    prepdesk fill {slug} <your-file>.json

`fill` validates every value against the schema, runs the arithmetic checks, and
rebuilds the keying sheet. Anything that does not survive validation is reported,
not silently dropped.
"""


def build(vault: Vault, client: Client, documents: list[Document],
          smap: ScreenMap, include_identifiers: bool = False) -> dict[str, Path]:
    pdir = vault.sub(client.slug, "packet")
    docs_dir = pdir / "documents"
    docs_dir.mkdir(parents=True, exist_ok=True)
    text_dir = vault.sub(client.slug, "text")

    screens_used = {d.drake_screen.upper() for d in documents if d.drake_screen}
    # Always include the single-instance screens; they have no document behind them
    # but still need keying.
    screens_used |= {s.code.upper() for s in smap.screens if not s.multi}

    index_lines = [
        f"# Documents — {client.name} · {client.form} · TY{client.year}",
        "",
        "| WP ref | Type | Drake screen | Text file | Readable |",
        "|---|---|---|---|---|",
    ]
    written = 0
    for doc in sorted(documents, key=lambda d: d.ref):
        src = text_dir / f"{doc.ref}.txt"
        readable = "no"
        if src.exists() and not doc.needs_ocr:
            text = src.read_text(encoding="utf-8", errors="replace")[:MAX_DOC_CHARS]
            if not include_identifiers:
                text = mask_text(text)
            header = (f"=== WP {doc.ref} | {doc.doc_type} | "
                      f"screen {doc.drake_screen or 'none'} | "
                      f"source_doc: {doc.staged_name} ===\n\n")
            write_private(docs_dir / f"{doc.ref}.txt", header + text)
            readable = "yes"
            written += 1
        index_lines.append(
            f"| {doc.ref} | {doc.doc_type} | {doc.drake_screen or '—'} | "
            f"`documents/{doc.ref}.txt` | {readable} |"
        )
    index_lines += ["", f"{written} of {len(documents)} documents carry readable text.", ""]

    paths = {
        "instructions": write_private(
            pdir / "PACKET.md",
            INSTRUCTIONS.format(label=client.label, slug=client.slug)),
        "schema": write_private(
            pdir / "schema.json",
            json.dumps(_schema(smap, screens_used), indent=2)),
        "documents": write_private(pdir / "documents.md", "\n".join(index_lines)),
    }

    if include_identifiers:
        write_private(pdir / "UNMASKED.txt",
                      "This packet contains unmasked taxpayer identifiers.\n"
                      f"Built {date.today().isoformat()}.\n"
                      "Do not send it anywhere you would not send the paper file.\n")
    return paths
