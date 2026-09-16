"""Drake screen maps: which fields exist on a screen and in what order.

The maps are TOML so a preparer can correct them without touching Python. Each
map carries a `verified` flag. It ships false, and it should stay false until
somebody has sat in front of their own Drake install and walked the screen
top to bottom against the file. The worksheet prints that status on every page
so nobody keys from an unverified map by accident.

A user copy in <vault>/screens/ overrides the packaged map of the same name.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path

PACKAGED_SCREENS = Path(__file__).resolve().parent.parent / "screens"

FIELD_TYPES = {"text", "ein", "ssn", "account", "money", "date", "code",
               "checkbox", "state", "zip", "percent", "int"}


@dataclass
class Field:
    id: str
    label: str
    type: str = "text"
    box: str = ""          # the box or line number printed on the paper form
    note: str = ""
    required: bool = False

    @property
    def display_box(self) -> str:
        return self.box or "—"


@dataclass
class Screen:
    code: str              # what you type at Drake's screen selector
    title: str
    fields: list[Field]
    doc_types: list[str] = field(default_factory=list)
    multi: bool = False    # one instance per source document
    order: int = 999
    note: str = ""
    wp_section: int = 200


@dataclass
class ScreenMap:
    form: str
    tax_year: int | None
    verified: bool
    source_note: str
    screens: list[Screen]
    path: Path
    limits: dict = field(default_factory=dict)

    def by_code(self, code: str) -> Screen | None:
        for s in self.screens:
            if s.code.upper() == code.upper():
                return s
        return None

    def for_doc_type(self, doc_type: str) -> Screen | None:
        for s in self.screens:
            if doc_type in s.doc_types:
                return s
        return None

    @property
    def status_line(self) -> str:
        if self.verified:
            return f"Screen map: {self.path.name} — VERIFIED against Drake {self.tax_year or ''}".strip()
        return (f"Screen map: {self.path.name} — **UNVERIFIED**. Field order mirrors the "
                "IRS form. Confirm against your Drake install before keying, then set "
                "verified = true in the map.")


def map_path(form: str, vault_root: Path | None = None) -> Path:
    name = f"{form.lower()}.toml"
    if vault_root:
        user = Path(vault_root) / "screens" / name
        if user.exists():
            return user
    packaged = PACKAGED_SCREENS / name
    if not packaged.exists():
        raise FileNotFoundError(
            f"no screen map for form {form}. Expected {packaged} or a copy in "
            f"{vault_root}/screens/ if you have a vault override."
        )
    return packaged


def load_map(form: str, vault_root: Path | None = None) -> ScreenMap:
    path = map_path(form, vault_root)
    with open(path, "rb") as fh:
        raw = tomllib.load(fh)

    screens = []
    for s in raw.get("screens", []):
        fields = []
        for f in s.get("fields", []):
            ftype = f.get("type", "text")
            if ftype not in FIELD_TYPES:
                raise ValueError(
                    f"{path.name}: screen {s.get('code')} field {f.get('id')} "
                    f"has unknown type {ftype!r}. Valid: {', '.join(sorted(FIELD_TYPES))}"
                )
            fields.append(Field(
                id=f["id"], label=f["label"], type=ftype,
                box=str(f.get("box", "")), note=f.get("note", ""),
                required=bool(f.get("required", False)),
            ))
        screens.append(Screen(
            code=s["code"], title=s["title"], fields=fields,
            doc_types=list(s.get("doc_types", [])),
            multi=bool(s.get("multi", False)),
            order=int(s.get("order", 999)),
            note=s.get("note", ""),
            wp_section=int(s.get("wp_section", 200)),
        ))
    screens.sort(key=lambda s: (s.order, s.code))

    return ScreenMap(
        form=raw.get("form", form).upper(),
        tax_year=raw.get("tax_year"),
        verified=bool(raw.get("verified", False)),
        source_note=raw.get("source_note", ""),
        screens=screens,
        path=path,
        limits=raw.get("limits", {}),
    )


def install_user_copy(form: str, vault_root: Path) -> Path:
    """Copy the packaged map into the vault so the preparer can correct it."""
    src = PACKAGED_SCREENS / f"{form.lower()}.toml"
    dest_dir = Path(vault_root) / "screens"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    if dest.exists():
        raise FileExistsError(f"{dest} already exists — edit it in place")
    dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    return dest
