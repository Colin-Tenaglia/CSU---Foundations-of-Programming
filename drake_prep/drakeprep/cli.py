"""Command line for the prep desk."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from . import __version__, export as export_mod, packet as packet_mod
from .config import Client, Vault, DEFAULT_VAULT, CLIENT_DIRS
from .extract import available_tools
from .intake import load_documents, run_intake, save_documents
from .screens import install_user_copy, load_map
from .security import audit, enforce_offline, network_allowed, shred
from .values import (Entry, blank_entries, cross_check, load_entries,
                     merge_issues, save_entries, validate)
from .workpapers import write_workpapers
from .worksheet import write_worksheets

OK, WARN, BAD = "✓", "!", "✗"


def _vault(args) -> Vault:
    return Vault(args.vault)


def _client(vault: Vault, slug: str) -> Client:
    try:
        return vault.load_client(slug)
    except FileNotFoundError as exc:
        sys.exit(str(exc))


def _require_vault(vault: Vault) -> None:
    if not vault.exists():
        sys.exit(f"no vault at {vault.root}. Run: prepdesk init")


# ------------------------------------------------------------------ commands

def cmd_init(args) -> int:
    vault = _vault(args)
    root = vault.init()
    audit(vault.audit_log, "init", vault=str(root))
    print(f"{OK} vault ready at {root}")
    print("  clients/       one directory per client")
    print("  prepdesk.toml  vault settings")
    print("  audit.log      every command, append only")
    print("\nKeep this directory on encrypted storage, and not on the machine "
          "Drake runs on.")
    print(f"\nNext: prepdesk client add \"Smith, John\" --year {args.year_hint} --form 1040")
    return 0


def cmd_doctor(args) -> int:
    vault = _vault(args)
    print(f"Drake Prep Desk {__version__}")
    print(f"  network        {BAD + ' OPEN' if network_allowed() else OK + ' blocked'}")
    print(f"  vault          {vault.root} "
          f"{OK if vault.exists() else BAD + ' (run: prepdesk init)'}")

    tools = available_tools()
    print("\nText extraction:")
    for name, present in tools.items():
        mark = OK if present else WARN
        print(f"  {mark} {name}")
    if not (tools["pdftotext"] or tools["pypdf"]):
        print(f"\n  {WARN} No PDF text extractor. Install poppler-utils for "
              "`pdftotext`, or `pip install pypdf`.")
    if not (tools["tesseract"] or tools["ocrmypdf"]):
        print(f"  {WARN} No OCR. Scanned documents will flow through as open items. "
              "Install `ocrmypdf` and `tesseract-ocr` to read them.")

    print("\nScreen maps:")
    for form in ("1040", "1120S", "1065"):
        try:
            smap = load_map(form, vault.root if vault.exists() else None)
            mark = OK if smap.verified else WARN
            state = "verified" if smap.verified else "UNVERIFIED — walk it against Drake"
            print(f"  {mark} {form}  {len(smap.screens):>2} screens, "
                  f"{sum(len(s.fields) for s in smap.screens):>3} fields  ({state})")
        except (FileNotFoundError, ValueError) as exc:
            print(f"  {BAD} {form}  {exc}")

    if vault.exists():
        clients = vault.list_clients()
        print(f"\nClients: {len(clients)}")
        for c in clients:
            docs = len(list(vault.sub(c.slug, "docs").glob("*")))
            print(f"  {c.slug:<28} {c.label:<36} {docs:>4} documents")
    return 0


def cmd_client_add(args) -> int:
    vault = _vault(args)
    _require_vault(vault)
    try:
        client = vault.add_client(args.name, args.year, args.form, args.notes or "")
    except ValueError as exc:
        sys.exit(str(exc))
    audit(vault.audit_log, "client_add", client=client.slug, form=client.form,
          year=client.year)
    print(f"{OK} {client.slug} — {client.label}")
    for name, purpose in CLIENT_DIRS.items():
        print(f"    {name:<8} {purpose}")
    print(f"\nNext: prepdesk intake {client.slug} \"/path/to/client documents\"")
    return 0


def cmd_clients(args) -> int:
    vault = _vault(args)
    _require_vault(vault)
    clients = vault.list_clients()
    if not clients:
        print("No clients yet. Run: prepdesk client add \"Name\" --year 2025 --form 1040")
        return 0
    for c in clients:
        docs = len(list(vault.sub(c.slug, "docs").glob("*")))
        filled = len(load_entries(vault, c))
        print(f"{c.slug:<28} {c.label:<36} {docs:>4} docs  {filled:>4} entries")
    return 0


def cmd_intake(args) -> int:
    vault = _vault(args)
    _require_vault(vault)
    client = _client(vault, args.slug)
    source = Path(args.folder).expanduser()

    print(f"Reading {source} …")
    try:
        documents = run_intake(vault, client, source,
                               allow_ocr=not args.no_ocr,
                               do_extract=not args.no_extract)
    except (NotADirectoryError, OSError) as exc:
        sys.exit(str(exc))

    if not documents:
        print(f"{WARN} no documents found under {source}")
        return 1

    audit(vault.audit_log, "intake", client=client.slug, source=str(source),
          documents=len(documents))

    by_section: dict[str, int] = {}
    for d in documents:
        by_section[d.section_name] = by_section.get(d.section_name, 0) + 1
    print(f"\n{OK} staged {len(documents)} documents into {vault.sub(client.slug, 'docs')}")
    for section, n in by_section.items():
        print(f"    {n:>4}  {section}")

    ocr = [d for d in documents if d.needs_ocr]
    unknown = [d for d in documents if d.confidence == "none"]
    guessed = [d for d in documents if d.confidence == "filename"]
    if ocr:
        print(f"\n{WARN} {len(ocr)} could not be read (scanned or unsupported):")
        for d in ocr[:10]:
            print(f"    WP {d.ref}  {d.original_name}  — {d.extract_note}")
        if len(ocr) > 10:
            print(f"    … and {len(ocr) - 10} more")
    if unknown:
        print(f"\n{WARN} {len(unknown)} not identified — set the type by hand:")
        for d in unknown[:10]:
            print(f"    WP {d.ref}  {d.original_name}")
    if guessed:
        print(f"\n{WARN} {len(guessed)} identified from the filename only. "
              "Confirm against the document.")

    print(f"\nThe source folder was not modified.")
    print(f"Next: prepdesk index {client.slug}")
    return 0


def cmd_index(args) -> int:
    vault = _vault(args)
    _require_vault(vault)
    client = _client(vault, args.slug)
    documents = _load_docs(vault, client)
    smap = load_map(client.form, vault.root)
    entries = load_entries(vault, client)
    issues = merge_issues(validate(smap, entries),
                          cross_check(smap, entries, smap.limits))

    paths = write_workpapers(vault, client, documents, smap, entries, issues)
    audit(vault.audit_log, "index", client=client.slug, documents=len(documents))

    print(f"{OK} workpaper index   {paths['index']}")
    print(f"{OK} tie-out shell     {paths['tie_out']}")
    print(f"{OK} open items        {paths['open_items']}")

    from .classify import gaps
    missing = gaps(client.form, {d.doc_type for d in documents})
    if missing:
        print(f"\n{WARN} {len(missing)} expected documents not in the file:")
        for m in missing:
            print(f"    {m}")
    print(f"\nNext: prepdesk packet {client.slug}")
    return 0


def cmd_packet(args) -> int:
    vault = _vault(args)
    _require_vault(vault)
    client = _client(vault, args.slug)
    documents = _load_docs(vault, client)
    smap = load_map(client.form, vault.root)

    paths = packet_mod.build(vault, client, documents, smap,
                             include_identifiers=args.include_identifiers)
    audit(vault.audit_log, "packet", client=client.slug,
          unmasked=args.include_identifiers)

    pdir = vault.sub(client.slug, "packet")
    print(f"{OK} packet at {pdir}")
    for name, path in paths.items():
        print(f"    {name:<14} {path.name}")
    if args.include_identifiers:
        print(f"\n{BAD} This packet contains UNMASKED identifiers. Treat it as the "
              "paper file.")
    else:
        print("\nIdentifiers are masked. SSN, EIN, and account fields are keyed by "
              "hand from the paper.")
    print(f"\nHand {pdir}/PACKET.md to Claude, then:")
    print(f"    prepdesk fill {client.slug} <claude-output>.json")
    return 0


def cmd_fill(args) -> int:
    vault = _vault(args)
    _require_vault(vault)
    client = _client(vault, args.slug)
    smap = load_map(client.form, vault.root)
    documents = _load_docs(vault, client)

    src = Path(args.json_file).expanduser()
    try:
        payload = json.loads(src.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        sys.exit(f"cannot read {src}: {exc}")

    raw_entries = payload.get("entries", payload if isinstance(payload, list) else [])
    if not raw_entries:
        sys.exit(f"no entries in {src}. Expected {{\"entries\": [...]}}")

    entries, rejected = [], []
    for raw in raw_entries:
        try:
            entries.append(Entry(
                screen=str(raw["screen"]),
                instance=int(raw.get("instance", 1)),
                wp_ref=raw.get("wp_ref"),
                source_doc=str(raw.get("source_doc", "")),
                values={k: str(v) for k, v in (raw.get("values") or {}).items()},
                confidence={k: str(v) for k, v in (raw.get("confidence") or {}).items()},
                notes=str(raw.get("notes", "")),
            ))
        except (KeyError, TypeError, ValueError) as exc:
            rejected.append(f"{raw!r:.80} — {exc}")

    if args.merge:
        existing = {e.key(): e for e in load_entries(vault, client)}
        for e in entries:
            existing[e.key()] = e
        entries = sorted(existing.values(), key=lambda e: (e.screen, e.instance))

    save_entries(vault, client, entries)
    issues = merge_issues(validate(smap, entries),
                          cross_check(smap, entries, smap.limits))
    paths = write_worksheets(vault, client, smap, entries)
    write_workpapers(vault, client, documents, smap, entries, issues)
    audit(vault.audit_log, "fill", client=client.slug, entries=len(entries),
          rejected=len(rejected))

    print(f"{OK} {len(entries)} entries loaded from {src.name}")
    if rejected:
        print(f"{BAD} {len(rejected)} rejected:")
        for r in rejected[:10]:
            print(f"    {r}")
    _report_issues(issues)
    print(f"\n{OK} worksheet     {paths['worksheet']}")
    print(f"{OK} keying sheet  {paths['keying_sheet']}")
    print(f"{OK} open items    {vault.sub(client.slug, 'out') / 'open_items.md'}")
    return 1 if any(i.severity == "blocker" for i in issues) else 0


def cmd_worksheet(args) -> int:
    vault = _vault(args)
    _require_vault(vault)
    client = _client(vault, args.slug)
    smap = load_map(client.form, vault.root)
    documents = _load_docs(vault, client)
    entries = load_entries(vault, client)
    if not entries:
        entries = blank_entries(smap, documents)
        save_entries(vault, client, entries)
        print(f"{WARN} no extracted values yet — wrote a blank skeleton "
              f"({len(entries)} screen instances)")
    paths = write_worksheets(vault, client, smap, entries)
    audit(vault.audit_log, "worksheet", client=client.slug, entries=len(entries))
    for name, path in paths.items():
        print(f"{OK} {name:<14} {path}")
    if not smap.verified:
        print(f"\n{WARN} {smap.path.name} is unverified. Walk it against Drake, "
              "correct anything that differs, then set verified = true.")
    return 0


def cmd_check(args) -> int:
    vault = _vault(args)
    _require_vault(vault)
    client = _client(vault, args.slug)
    smap = load_map(client.form, vault.root)
    documents = _load_docs(vault, client)
    entries = load_entries(vault, client)
    if not entries:
        sys.exit(f"nothing to check — no values for {client.slug}. "
                 f"Run: prepdesk fill {client.slug} <file>.json")
    issues = merge_issues(validate(smap, entries),
                          cross_check(smap, entries, smap.limits))
    write_workpapers(vault, client, documents, smap, entries, issues)
    audit(vault.audit_log, "check", client=client.slug, issues=len(issues))
    _report_issues(issues, verbose=True)
    return 1 if any(i.severity == "blocker" for i in issues) else 0


def cmd_export(args) -> int:
    vault = _vault(args)
    _require_vault(vault)
    client = _client(vault, args.slug)
    smap = load_map(client.form, vault.root)
    entries = load_entries(vault, client)

    if args.format in export_mod.NOT_SUPPORTED:
        print(f"{WARN} {export_mod.NOT_SUPPORTED[args.format]}")
        return 1
    if args.format == "8949":
        path, n = export_mod.export_8949(vault, client, entries)
        print(f"{OK} {n} capital transactions -> {path}")
        print(f"\n{WARN} Confirm the column order against Drake's Form 8949 Import "
              "dialog before the first use. Import once, check what landed where, and "
              "correct COLUMNS_8949 in drakeprep/export.py if it differs.")
    elif args.format == "csv":
        path, n = export_mod.export_flat_csv(vault, client, smap, entries)
        print(f"{OK} {n} values -> {path}")
    else:
        paths = write_worksheets(vault, client, smap, entries)
        print(f"{OK} keying sheet -> {paths['keying_sheet']}")
    audit(vault.audit_log, "export", client=client.slug, format=args.format)
    return 0


def cmd_screens(args) -> int:
    vault = _vault(args)
    if args.install:
        try:
            dest = install_user_copy(args.form, vault.root)
        except (FileExistsError, FileNotFoundError) as exc:
            sys.exit(str(exc))
        print(f"{OK} copied to {dest}")
        print("Edit it there. The vault copy overrides the packaged map.")
        return 0

    smap = load_map(args.form, vault.root if vault.exists() else None)
    print(f"{smap.form}  ·  {smap.path}")
    print(f"{smap.status_line}\n")
    for s in smap.screens:
        multi = " (one per document)" if s.multi else ""
        print(f"  {s.code:<6} {s.title}{multi}")
        if args.fields:
            for f in s.fields:
                req = " *" if f.required else ""
                print(f"           {f.display_box:<8} {f.id:<32} {f.type:<9} "
                      f"{f.label}{req}")
    return 0


def cmd_purge(args) -> int:
    vault = _vault(args)
    _require_vault(vault)
    client = _client(vault, args.slug)
    cdir = vault.client_dir(client.slug)
    files = [p for p in cdir.rglob("*") if p.is_file()]

    print(f"About to destroy {len(files)} files under {cdir}")
    print(f"  {client.label}")
    if not args.yes:
        reply = input(f"Type the client slug to confirm ({client.slug}): ").strip()
        if reply != client.slug:
            print("Cancelled. Nothing was deleted.")
            return 1

    destroyed = sum(1 for p in files if shred(p))
    shutil.rmtree(cdir, ignore_errors=True)
    audit(vault.audit_log, "purge", client=client.slug, files=destroyed)
    print(f"{OK} overwrote and removed {destroyed} of {len(files)} files")
    if destroyed < len(files):
        print(f"{WARN} {len(files) - destroyed} could not be overwritten before removal")
    print("\nOverwriting does not reliably reach the original blocks on flash storage "
          "or a copy-on-write filesystem. Full-disk encryption is the control that "
          "actually holds.")
    return 0


def cmd_audit(args) -> int:
    vault = _vault(args)
    if not vault.audit_log.exists():
        print("No audit log yet.")
        return 0
    lines = vault.audit_log.read_text(encoding="utf-8").splitlines()
    for line in lines[-args.tail:]:
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        detail = " ".join(f"{k}={v}" for k, v in e.items()
                          if k not in ("ts", "action", "user"))
        print(f"{e['ts']}  {e['action']:<12} {detail}")
    return 0


# ------------------------------------------------------------------ helpers

def _load_docs(vault: Vault, client: Client):
    try:
        return load_documents(vault, client)
    except FileNotFoundError as exc:
        sys.exit(str(exc))


def _report_issues(issues, verbose: bool = False) -> None:
    blockers = [i for i in issues if i.severity == "blocker"]
    checks = [i for i in issues if i.severity == "check"]
    notes = [i for i in issues if i.severity == "note"]
    print(f"\n{len(blockers)} blockers · {len(checks)} to check · {len(notes)} noted")
    limit = 10_000 if verbose else 12
    for group, mark in ((blockers, BAD), (checks, WARN), (notes, " ")):
        for i in group[:limit]:
            print(f"  {mark} {i.line()}")
        if len(group) > limit:
            print(f"    … and {len(group) - limit} more — see out/open_items.md")


# ------------------------------------------------------------------ parser

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="prepdesk",
        description="Offline tax document intake and Drake-ordered data entry prep.")
    p.add_argument("--vault", default=str(DEFAULT_VAULT),
                   help=f"vault directory (default {DEFAULT_VAULT})")
    p.add_argument("--version", action="version", version=f"prepdesk {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("init", help="create the vault")
    s.add_argument("--year-hint", default="2025", help=argparse.SUPPRESS)
    s.set_defaults(func=cmd_init)

    s = sub.add_parser("doctor", help="report what is installed and what is missing")
    s.set_defaults(func=cmd_doctor)

    s = sub.add_parser("clients", help="list clients")
    s.set_defaults(func=cmd_clients)

    s = sub.add_parser("client", help="client records")
    csub = s.add_subparsers(dest="client_command", required=True)
    a = csub.add_parser("add", help="add a client")
    a.add_argument("name")
    a.add_argument("--year", type=int, required=True)
    a.add_argument("--form", required=True, choices=["1040", "1120S", "1120s", "1065"])
    a.add_argument("--notes", default="")
    a.set_defaults(func=cmd_client_add)

    s = sub.add_parser("intake", help="stage a document folder into the vault")
    s.add_argument("slug")
    s.add_argument("folder")
    s.add_argument("--no-ocr", action="store_true", help="skip OCR on scanned documents")
    s.add_argument("--no-extract", action="store_true",
                   help="copy and classify only, do not read text")
    s.set_defaults(func=cmd_intake)

    s = sub.add_parser("index", help="build the workpaper index, gaps, and tie-out")
    s.add_argument("slug")
    s.set_defaults(func=cmd_index)

    s = sub.add_parser("packet", help="build the bundle to hand to Claude")
    s.add_argument("slug")
    s.add_argument("--include-identifiers", action="store_true",
                   help="do not mask SSN, EIN, and account numbers")
    s.set_defaults(func=cmd_packet)

    s = sub.add_parser("fill", help="load extracted values back in")
    s.add_argument("slug")
    s.add_argument("json_file")
    s.add_argument("--merge", action="store_true",
                   help="merge into existing values instead of replacing")
    s.set_defaults(func=cmd_fill)

    s = sub.add_parser("worksheet", help="render the Drake-ordered worksheets")
    s.add_argument("slug")
    s.set_defaults(func=cmd_worksheet)

    s = sub.add_parser("check", help="re-run validation and the arithmetic checks")
    s.add_argument("slug")
    s.set_defaults(func=cmd_check)

    s = sub.add_parser("export", help="write a file for Drake or for review")
    s.add_argument("slug")
    s.add_argument("--format", default="keying",
                   choices=["keying", "csv", "8949", "w2", "4562", "k1"])
    s.set_defaults(func=cmd_export)

    s = sub.add_parser("screens", help="show or install a Drake screen map")
    s.add_argument("form", choices=["1040", "1120S", "1120s", "1065"])
    s.add_argument("--fields", action="store_true", help="list every field")
    s.add_argument("--install", action="store_true",
                   help="copy the map into the vault so you can edit it")
    s.set_defaults(func=cmd_screens)

    s = sub.add_parser("purge", help="overwrite and remove a client's files")
    s.add_argument("slug")
    s.add_argument("--yes", action="store_true", help="skip the confirmation prompt")
    s.set_defaults(func=cmd_purge)

    s = sub.add_parser("audit", help="show the audit log")
    s.add_argument("--tail", type=int, default=40)
    s.set_defaults(func=cmd_audit)

    return p


def main(argv=None) -> int:
    enforce_offline()
    args = build_parser().parse_args(argv)
    if getattr(args, "form", None):
        args.form = args.form.upper()
    return args.func(args)
