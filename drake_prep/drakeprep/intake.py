"""Stage documents into the vault, classify them, and assign workpaper refs.

Source documents are copied, never moved and never edited. The original folder is
left exactly as found, which is the rule that makes this safe to point at a live
client directory.
"""

from __future__ import annotations

import csv
import json
import os
import re
import shutil
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

from . import classify as classify_mod
from . import extract as extract_mod
from .config import Client, Vault, FILE_MODE, write_private
from .security import fingerprint, mask_text


@dataclass
class Document:
    ref: int
    doc_type: str
    wp_section: int
    section_name: str
    drake_screen: str | None
    confidence: str
    evidence: str
    original_name: str
    original_path: str
    staged_name: str
    ext: str
    size_bytes: int
    modified: str
    sha256_16: str
    extract_method: str = "none"
    needs_ocr: bool = True
    extract_note: str = ""
    ties_to: str = ""

    @property
    def flag(self) -> str:
        if self.needs_ocr:
            return "OCR"
        if self.confidence == "none":
            return "CLASSIFY"
        if self.confidence == "filename":
            return "CHECK"
        return ""


def _stage_name(ref: int, doc_type: str, original: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", Path(original).stem.lower()).strip("-")[:40]
    kind = re.sub(r"[^A-Za-z0-9]+", "", doc_type)[:12] or "DOC"
    return f"{ref}_{kind}_{slug or 'doc'}{Path(original).suffix.lower()}"


def run_intake(vault: Vault, client: Client, source: Path,
               allow_ocr: bool = True, do_extract: bool = True) -> list[Document]:
    """Walk `source`, copy every document in, extract text, classify, assign refs."""
    source = Path(source).expanduser().resolve()
    if not source.is_dir():
        raise NotADirectoryError(f"not a directory: {source}")

    docs_dir = vault.sub(client.slug, "docs")
    text_dir = vault.sub(client.slug, "text")
    work_dir = vault.sub(client.slug, "work")
    for d in (docs_dir, text_dir, work_dir):
        d.mkdir(parents=True, exist_ok=True)

    found: list[tuple[Path, str]] = []
    for dirpath, dirnames, filenames in os.walk(source):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for fn in sorted(filenames):
            if classify_mod.should_skip(fn):
                continue
            p = Path(dirpath) / fn
            if p.is_file():
                found.append((p, str(p.relative_to(source))))

    if not found:
        return []

    # Pass 1: extract text so classification has real evidence to work with.
    staged: list[dict] = []
    for path, rel in found:
        ex = extract_mod.Extraction("", "none", True, "extraction skipped")
        if do_extract:
            ex = extract_mod.extract(path, workdir=work_dir, allow_ocr=allow_ocr)
        verdict = classify_mod.classify(rel, ex.text)
        st = path.stat()
        staged.append({
            "path": path, "rel": rel, "ex": ex, "verdict": verdict,
            "size": st.st_size,
            "modified": datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d"),
        })

    # Pass 2: refs are sequential within a section, ordered by type then name, so
    # rerunning intake on the same folder produces the same numbering.
    staged.sort(key=lambda s: (s["verdict"].wp_section, s["verdict"].doc_type,
                               s["rel"].lower()))
    counter: dict[int, int] = {}
    documents: list[Document] = []
    for s in staged:
        v = s["verdict"]
        n = counter.get(v.wp_section, 0)
        counter[v.wp_section] = n + 1
        ref = v.wp_section + n
        staged_name = _stage_name(ref, v.doc_type, s["rel"])

        dest = docs_dir / staged_name
        shutil.copy2(s["path"], dest)
        os.chmod(dest, FILE_MODE)

        if s["ex"].text.strip():
            write_private(text_dir / f"{ref}.txt", s["ex"].text)

        documents.append(Document(
            ref=ref,
            doc_type=v.doc_type,
            wp_section=v.wp_section,
            section_name=classify_mod.SECTIONS[v.wp_section],
            drake_screen=v.drake_screen,
            confidence=v.confidence,
            evidence=v.evidence,
            original_name=Path(s["rel"]).name,
            original_path=s["rel"],
            staged_name=staged_name,
            ext=s["path"].suffix.lower().lstrip("."),
            size_bytes=s["size"],
            modified=s["modified"],
            sha256_16=fingerprint(s["path"]),
            extract_method=s["ex"].method,
            needs_ocr=s["ex"].needs_ocr,
            extract_note=s["ex"].note,
        ))

    save_documents(vault, client, documents)
    write_manifest(vault, client, documents, source)
    return documents


def save_documents(vault: Vault, client: Client, documents: list[Document]) -> Path:
    path = vault.sub(client.slug, "work") / "documents.json"
    return write_private(path, json.dumps([asdict(d) for d in documents], indent=2))


def load_documents(vault: Vault, client: Client) -> list[Document]:
    path = vault.sub(client.slug, "work") / "documents.json"
    if not path.exists():
        raise FileNotFoundError(
            f"no intake yet for {client.slug}. Run: prepdesk intake {client.slug} <folder>"
        )
    return [Document(**d) for d in json.loads(path.read_text(encoding="utf-8"))]


def write_manifest(vault: Vault, client: Client, documents: list[Document],
                   source: Path) -> Path:
    path = vault.sub(client.slug, "work") / "manifest.csv"
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["ref", "doc_type", "section", "staged_name", "original_path",
                    "size_bytes", "modified", "sha256_16", "extract_method",
                    "needs_ocr", "confidence"])
        for d in documents:
            w.writerow([d.ref, d.doc_type, d.section_name, d.staged_name,
                        mask_text(d.original_path), d.size_bytes, d.modified,
                        d.sha256_16, d.extract_method, "yes" if d.needs_ocr else "no",
                        d.confidence])
    os.chmod(path, FILE_MODE)
    return path
