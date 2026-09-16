"""Pull text out of a source document, locally.

Every path here is a local process. Nothing leaves the machine. When no extractor
is available the document is marked `needs_ocr` and flows through the rest of the
pipeline as an open item rather than silently producing an empty worksheet.

Preference order, best first:
  pdftotext (poppler)   fast, accurate on digital PDFs
  pypdf                 pure python fallback
  ocrmypdf / tesseract  scans and photographs
"""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

TEXT_EXT = {".txt", ".md", ".csv", ".tsv", ".json"}
PDF_EXT = {".pdf"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".heic", ".webp"}

# A digital PDF page normally yields far more than this. Less means it is a scan.
MIN_CHARS_PER_PAGE = 60


@dataclass
class Extraction:
    text: str
    method: str          # pdftotext | pypdf | plain | tesseract | none
    needs_ocr: bool
    note: str = ""

    @property
    def ok(self) -> bool:
        return bool(self.text.strip()) and not self.needs_ocr


def _have(binary: str) -> bool:
    return shutil.which(binary) is not None


def available_tools() -> dict[str, bool]:
    tools = {
        "pdftotext": _have("pdftotext"),
        "tesseract": _have("tesseract"),
        "ocrmypdf": _have("ocrmypdf"),
        "pypdf": False,
    }
    try:
        import pypdf  # noqa: F401
        tools["pypdf"] = True
    except ImportError:
        pass
    return tools


def _pdftotext(path: Path) -> str | None:
    if not _have("pdftotext"):
        return None
    try:
        res = subprocess.run(
            ["pdftotext", "-layout", "-q", str(path), "-"],
            capture_output=True, timeout=120,
        )
        return res.stdout.decode("utf-8", "replace")
    except (OSError, subprocess.SubprocessError):
        return None


def _pypdf(path: Path) -> str | None:
    try:
        from pypdf import PdfReader
    except ImportError:
        return None
    try:
        reader = PdfReader(str(path))
        return "\n".join((p.extract_text() or "") for p in reader.pages)
    except Exception:
        return None


def _ocr_image(path: Path) -> str | None:
    if not _have("tesseract"):
        return None
    try:
        res = subprocess.run(
            ["tesseract", str(path), "stdout"],
            capture_output=True, timeout=300,
        )
        return res.stdout.decode("utf-8", "replace")
    except (OSError, subprocess.SubprocessError):
        return None


def _ocr_pdf(path: Path, workdir: Path) -> str | None:
    if not _have("ocrmypdf"):
        return None
    out = workdir / (path.stem + ".ocr.pdf")
    try:
        subprocess.run(
            ["ocrmypdf", "--force-ocr", "--quiet", str(path), str(out)],
            capture_output=True, timeout=900, check=True,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return _pdftotext(out) or _pypdf(out)


def extract(path: Path, workdir: Path | None = None, allow_ocr: bool = True) -> Extraction:
    ext = path.suffix.lower()
    workdir = workdir or path.parent

    if ext in TEXT_EXT:
        try:
            return Extraction(path.read_text(encoding="utf-8", errors="replace"),
                              "plain", False)
        except OSError as exc:
            return Extraction("", "none", True, f"unreadable: {exc}")

    if ext in PDF_EXT:
        text = _pdftotext(path)
        method = "pdftotext"
        if text is None:
            text, method = _pypdf(path), "pypdf"
        if text is None:
            return Extraction("", "none", True,
                              "no PDF text extractor installed (pdftotext or pypdf)")
        pages = max(1, text.count("\f") or 1)
        if len(text.strip()) < MIN_CHARS_PER_PAGE * pages:
            if allow_ocr:
                ocr = _ocr_pdf(path, workdir)
                if ocr and len(ocr.strip()) > len(text.strip()):
                    return Extraction(ocr, "ocrmypdf", False, "scanned PDF, OCR applied")
            return Extraction(text, method, True,
                              "little or no embedded text — scanned document, OCR needed")
        return Extraction(text, method, False)

    if ext in IMAGE_EXT:
        if allow_ocr:
            ocr = _ocr_image(path)
            if ocr and ocr.strip():
                return Extraction(ocr, "tesseract", False, "image OCR")
        return Extraction("", "none", True, "image with no OCR available")

    return Extraction("", "none", True, f"unsupported file type: {ext or 'none'}")
