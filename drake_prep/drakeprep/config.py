"""Vault layout, client records, and defaults.

A vault is a single directory that holds every client the desk knows about.
Nothing is written outside it. Keep the vault on encrypted storage that is not
the machine Drake runs on.
"""

from __future__ import annotations

import json
import os
import re
import unicodedata
from dataclasses import dataclass, asdict, field
from datetime import date
from pathlib import Path

DEFAULT_VAULT = Path(os.environ.get("PREPDESK_VAULT", "~/PrepDesk")).expanduser()

FORMS = ("1040", "1120S", "1065")

# Directories created under clients/<slug>/. Values are the purpose, used by
# `prepdesk doctor` when it reports on a client.
CLIENT_DIRS = {
    "docs": "staged source documents, renamed to their workpaper ref",
    "text": "extracted text, one file per document",
    "work": "workpaper index, manifest, gaps, tie-out",
    "out": "Drake-ordered worksheets and keying sheets",
    "packet": "the bundle handed to Claude",
}

DIR_MODE = 0o700
FILE_MODE = 0o600


def slugify(name: str) -> str:
    """'Smith, John & Mary' -> 'smith-john-mary'."""
    norm = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    norm = re.sub(r"[^a-zA-Z0-9]+", "-", norm).strip("-").lower()
    return norm or "client"


@dataclass
class Client:
    slug: str
    name: str
    year: int
    form: str
    created: str = field(default_factory=lambda: date.today().isoformat())
    notes: str = ""

    @property
    def label(self) -> str:
        return f"{self.name} · {self.form} · TY{self.year}"


class Vault:
    """Filesystem layout. Every path the app touches comes from here."""

    def __init__(self, root: Path | str = DEFAULT_VAULT):
        self.root = Path(root).expanduser().resolve()

    # -- paths ---------------------------------------------------------
    @property
    def clients_dir(self) -> Path:
        return self.root / "clients"

    @property
    def audit_log(self) -> Path:
        return self.root / "audit.log"

    @property
    def config_file(self) -> Path:
        return self.root / "prepdesk.toml"

    def client_dir(self, slug: str) -> Path:
        return self.clients_dir / slug

    def sub(self, slug: str, name: str) -> Path:
        if name not in CLIENT_DIRS:
            raise KeyError(f"unknown client subdirectory: {name}")
        return self.client_dir(slug) / name

    # -- lifecycle -----------------------------------------------------
    def init(self) -> Path:
        self.root.mkdir(parents=True, exist_ok=True)
        os.chmod(self.root, DIR_MODE)
        self.clients_dir.mkdir(exist_ok=True)
        os.chmod(self.clients_dir, DIR_MODE)
        if not self.config_file.exists():
            self.config_file.write_text(
                "# Drake Prep Desk vault\n"
                f'created = "{date.today().isoformat()}"\n'
                "# Assisted mode sends document text to the Claude API.\n"
                "# Leave false to keep this desk fully offline.\n"
                "assisted_mode_allowed = false\n",
                encoding="utf-8",
            )
            os.chmod(self.config_file, FILE_MODE)
        return self.root

    def exists(self) -> bool:
        return self.clients_dir.is_dir()

    # -- client records ------------------------------------------------
    def add_client(self, name: str, year: int, form: str, notes: str = "") -> Client:
        form = form.upper().replace("-", "")
        if form not in FORMS:
            raise ValueError(f"form must be one of {', '.join(FORMS)}")
        slug = f"{slugify(name)}-{year}"
        client = Client(slug=slug, name=name, year=int(year), form=form, notes=notes)
        cdir = self.client_dir(slug)
        cdir.mkdir(parents=True, exist_ok=True)
        os.chmod(cdir, DIR_MODE)
        for sub in CLIENT_DIRS:
            d = cdir / sub
            d.mkdir(exist_ok=True)
            os.chmod(d, DIR_MODE)
        self.save_client(client)
        return client

    def save_client(self, client: Client) -> Path:
        path = self.client_dir(client.slug) / "client.json"
        path.write_text(json.dumps(asdict(client), indent=2), encoding="utf-8")
        os.chmod(path, FILE_MODE)
        return path

    def load_client(self, slug: str) -> Client:
        path = self.client_dir(slug) / "client.json"
        if not path.exists():
            raise FileNotFoundError(
                f"no client '{slug}' in {self.root}. Run: prepdesk clients"
            )
        return Client(**json.loads(path.read_text(encoding="utf-8")))

    def list_clients(self) -> list[Client]:
        if not self.clients_dir.is_dir():
            return []
        out = []
        for d in sorted(self.clients_dir.iterdir()):
            if (d / "client.json").exists():
                out.append(self.load_client(d.name))
        return out


def write_private(path: Path, text: str) -> Path:
    """Write a file readable only by its owner."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    os.chmod(path, FILE_MODE)
    return path
