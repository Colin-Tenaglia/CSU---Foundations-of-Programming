# Drake Prep Desk

A standalone, offline desk for tax document intake. You drop a client's documents
into a folder, and it stages them, indexes them as workpapers, tells you what is
missing, and produces a data entry worksheet ordered the way Drake's screens are
ordered — so keying the return is reading down a page instead of hunting through a
pile of PDFs.

It runs on its own machine. Nothing it does touches the machine Drake runs on, and
nothing leaves the disk unless you carry it.

```
client folder  →  intake  →  workpaper index + gaps
                     ↓
                  packet  →  Claude  →  values.json
                     ↓
              keying sheet (Drake screen order) + open items + tie-out
```

## Why it is built this way

**Offline is enforced, not promised.** `security.enforce_offline()` replaces
`socket.connect` before the CLI parses an argument. An accidental network call
raises instead of sending. There is no API key, no telemetry, and no assisted mode
in this version.

**The extraction step is a file hand-off, not a service.** The app writes a packet;
you hand the packet to Claude however you want; Claude's answer comes back as one
JSON file. The desk never calls anything. That seam is what lets the documents sit
on a machine with no network at all.

**Identifiers are masked before they reach the packet.** SSNs, EINs, and account
numbers read as `***-**-9087`. A model does not need an SSN to read box 1 of a W-2,
and a preparer keys those from the paper anyway. Unmasked values live only in
`out/values.json`, mode `0600`, which never enters a packet.

**Every command is logged and nothing is moved.** Source documents are copied, never
moved and never edited, so the desk is safe to point at a live client folder.

## Install

Python 3.11 or newer. No required dependencies.

```bash
cd drake_prep
./prepdesk.py doctor
```

`doctor` reports what is installed. Two optional additions make it much better at
reading documents:

```bash
# PDF text — pick either
apt install poppler-utils        # gives you `pdftotext`, the faster path
pip install pypdf                # pure python fallback

# OCR for scans and photographs
apt install ocrmypdf tesseract-ocr
```

Without a PDF extractor every PDF becomes an open item. Nothing is silently
skipped — a document it cannot read shows up on the open-items list as a document
it cannot read.

## Workflow

```bash
./prepdesk.py init
./prepdesk.py client add "Smith, John and Mary" --year 2025 --form 1040

# Copy, classify, and extract text. The source folder is not modified.
./prepdesk.py intake smith-john-and-mary-2025 "/media/usb/Smith 2025"

# Workpaper index, the gaps list, and a tie-out shell.
./prepdesk.py index smith-john-and-mary-2025

# Build the bundle to hand to Claude.
./prepdesk.py packet smith-john-and-mary-2025

# ... Claude reads packet/PACKET.md and returns one JSON file ...

# Load it back. Validates every value, runs the checks, rebuilds the sheets.
./prepdesk.py fill smith-john-and-mary-2025 claude-output.json

# Key from out/keying_sheet.md, then work out/open_items.md.
```

Then, when the engagement is over:

```bash
./prepdesk.py purge smith-john-and-mary-2025
```

### What lands where

| Path | What it holds |
|---|---|
| `docs/` | staged copies, renamed to `<wp_ref>_<TYPE>_<name>` |
| `text/` | extracted text, one file per workpaper ref |
| `work/workpaper_index.md` | the index, by section, with the **Not in the file** list |
| `work/tie_out.md` | a tie-out shell — fill **Per return** after keying |
| `work/manifest.csv` | every document with size, date, and content hash |
| `out/worksheet.md` | every field on every screen, in Drake order |
| `out/keying_sheet.md` | only the fields that have values — this is the one you key from |
| `out/open_items.md` | what has to be answered before the return is signed |
| `out/values.json` | unmasked values, `0600`, never leaves the vault |
| `packet/` | what you hand to Claude |

Workpaper numbering follows the standard series so an index reads the same across
clients and years: **100** administrative, **200** income, **300** deductions,
**400** balance sheet, **500** fixed assets, **600** basis and equity, **700** state,
**800** review, **900** filed return.

## The screen maps

`screens/1040.toml`, `screens/1120s.toml`, and `screens/1065.toml` define which
fields appear on which Drake screen and in what order. They are TOML so you can
correct them without touching Python.

**They ship with `verified = false` and you should leave it false until you have
walked each screen against your own Drake install.** The field order here follows
the IRS form box order, which is how Drake lays out its information-return screens —
close, but transcribed from the forms, not confirmed against the software. Every
worksheet prints that status at the top so nobody keys from an unverified map by
accident.

To fix one:

```bash
./prepdesk.py screens 1040 --fields      # see what is in it
./prepdesk.py screens 1040 --install     # copy it into the vault, then edit
```

The vault copy overrides the packaged one. Set `verified = true` and record the
Drake year once you have checked it.

`[limits]` at the top of `screens/1040.toml` holds the figures the arithmetic checks
use — the social security wage base, the withholding rates, the SALT cap. They are
not updated automatically. Correct them for the year you are preparing.

## About "uploading to Drake"

Drake is not an open pipe. Per Drake's own documentation it imports Forms W-2, 4562,
and 8949, Schedules K-1 from a business return into an individual return, and
end-of-year balances. Of those, **the 8949 import is the only one with a file layout
a preparer can produce themselves** — CSV, tab-delimited, or Excel through the Form
8949 Import / GruntWorx Trades utility.

So this desk does one real export and is honest about the rest:

```bash
./prepdesk.py export <slug> --format 8949   # CSV for the 8949 import utility
./prepdesk.py export <slug> --format csv    # every value, flat, for review
./prepdesk.py export <slug> --format keying # the Markdown keying sheet
```

`--format w2`, `--format 4562`, and `--format k1` deliberately refuse and tell you
what to do instead. **Confirm the 8949 column order against the import dialog in your
Drake version before the first real use** — import once, look at what landed where,
and correct `COLUMNS_8949` in `drakeprep/export.py` if it differs.

Drake Portals (SecureFilePro) is for exchanging documents with clients. It is not an
import path for prepared values, and this desk does not touch it.

## The checks

`fill` and `check` run two passes.

**Validation** — types and required fields. A money field that is not a number, a
date that will not parse, an SSN that is not nine digits, a field that is not on the
screen at all.

**Arithmetic on the face of the document** — things the paper should satisfy by
itself:

- W-2 box 4 against box 3 × 6.2%, box 6 against box 5 × 1.45%, box 3 against the wage base
- 1099-DIV box 1b exceeding box 1a
- 1099-R box 2a exceeding box 1; a code 1 with no §72(t) exception noted
- Form 8949 holding period against the reported box
- Schedule C gross receipts below the 1099-NECs linked to it
- Schedule E personal use days against the §280A threshold
- An S corp loss with no Form 7203 in the file (§1366(d))
- A 1095-A with a zero column B and advance credit paid

Findings come out as **blockers** (stop the return), **checks** (someone has to
look), and **notes**. `fill` and `check` exit non-zero when a blocker is open, so
they work in a script.

A check firing is not proof of an error. It is proof that somebody needs to look.

## What this does not do

It does not prepare a return, compute tax, or give tax advice. It does not verify
that the amounts on a source document are correct, reach prior-year carryovers or
basis history, or check anything about the return as keyed into Drake. Values read
off scanned documents carry OCR risk, and every one of them needs a human read
against the paper before it is keyed.

The classification is pattern matching over document text and filenames. It is a
starting point. Open the index and fix what it got wrong — that review is part of
the workflow, not a sign something broke.

`purge` overwrites before unlinking, which closes the casual-recovery case. It does
not reliably reach the original blocks on flash storage or a copy-on-write
filesystem. Full-disk encryption is the control that actually holds.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

51 tests covering masking, the offline guard, classification, parsing, screen-map
integrity, every arithmetic check, and an end-to-end intake that asserts the source
folder comes out untouched.
