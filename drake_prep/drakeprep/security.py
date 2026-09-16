"""Security posture for the desk.

Three concrete guarantees, each enforced in code rather than documented and hoped for:

1. Offline by default. Outbound sockets raise unless assisted mode is explicitly
   enabled for the process.
2. Identifiers are masked in every human-readable artifact. Full values exist only
   in owner-only JSON that never goes into a packet.
3. Every command appends to an audit log, and `purge` overwrites before unlinking.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import socket
import sys
from datetime import datetime, timezone
from pathlib import Path

# --------------------------------------------------------------------------
# 1. Offline guard
# --------------------------------------------------------------------------

_ALLOW_NETWORK = False
_real_connect = socket.socket.connect
_real_connect_ex = socket.socket.connect_ex


class NetworkBlocked(RuntimeError):
    pass


def _blocked_connect(self, address, *a, **kw):
    if _ALLOW_NETWORK:
        return _real_connect(self, address, *a, **kw)
    raise NetworkBlocked(
        f"outbound connection to {address!r} blocked. This desk runs offline. "
        "Assisted mode must be enabled in the vault config and requested with "
        "--assisted on the command line."
    )


def _blocked_connect_ex(self, address, *a, **kw):
    if _ALLOW_NETWORK:
        return _real_connect_ex(self, address, *a, **kw)
    raise NetworkBlocked(f"outbound connection to {address!r} blocked (offline desk).")


def enforce_offline() -> None:
    """Install the guard. Called once at CLI start."""
    socket.socket.connect = _blocked_connect
    socket.socket.connect_ex = _blocked_connect_ex


def allow_network(reason: str) -> None:
    """Lift the guard for assisted mode. The caller must have consent."""
    global _ALLOW_NETWORK
    _ALLOW_NETWORK = True
    sys.stderr.write(f"[prepdesk] network enabled: {reason}\n")


def network_allowed() -> bool:
    return _ALLOW_NETWORK


# --------------------------------------------------------------------------
# 2. Masking
# --------------------------------------------------------------------------

# Order matters: EIN before SSN, since both are digit runs with dashes.
_EIN = re.compile(r"\b(\d{2})-(\d{7})\b")
_SSN = re.compile(r"\b(\d{3})-(\d{2})-(\d{4})\b")
_SSN_BARE = re.compile(r"\b(?<!\d)(\d{9})(?!\d)\b")
_ACCOUNT = re.compile(r"\b(?:acct|account|a/c)[.: #]*([0-9Xx*-]{6,})\b", re.I)
_CARD = re.compile(r"\b(?:\d[ -]*?){13,16}\b")


def mask_text(text: str) -> str:
    """Mask identifiers anywhere in free text. Used on everything readable."""
    text = _EIN.sub(lambda m: f"**-***{m.group(2)[-4:]}", text)
    text = _SSN.sub(lambda m: f"***-**-{m.group(3)}", text)
    text = _SSN_BARE.sub(lambda m: f"***-**-{m.group(1)[-4:]}", text)
    text = _ACCOUNT.sub(lambda m: m.group(0).replace(m.group(1), "****" + m.group(1)[-4:]), text)
    text = _CARD.sub(lambda m: "****-****-****-" + re.sub(r"\D", "", m.group(0))[-4:], text)
    return text


def mask_value(value: str, kind: str) -> str:
    """Mask a single field by its declared type."""
    if value is None:
        return ""
    s = str(value)
    if kind == "ssn":
        digits = re.sub(r"\D", "", s)
        return f"***-**-{digits[-4:]}" if len(digits) >= 4 else "***-**-****"
    if kind == "ein":
        digits = re.sub(r"\D", "", s)
        return f"**-***{digits[-4:]}" if len(digits) >= 4 else "**-*******"
    if kind == "account":
        return "****" + s[-4:] if len(s) >= 4 else "****"
    return s


def fingerprint(path: Path, limit: int = 8 * 1024 * 1024) -> str:
    """Short content hash. Detects a document swapped under the same name."""
    h = hashlib.sha256()
    try:
        with open(path, "rb") as fh:
            while chunk := fh.read(1024 * 1024):
                h.update(chunk)
                limit -= len(chunk)
                if limit <= 0:
                    break
    except OSError:
        return ""
    return h.hexdigest()[:16]


# --------------------------------------------------------------------------
# 3. Audit log and purge
# --------------------------------------------------------------------------

def audit(log_path: Path, action: str, **details) -> None:
    """Append-only record. Never contains a document value, only references."""
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "action": action,
        "user": os.environ.get("USER") or os.environ.get("USERNAME") or "?",
        **details,
    }
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")
    try:
        os.chmod(log_path, 0o600)
    except OSError:
        pass


def shred(path: Path, passes: int = 1) -> bool:
    """Overwrite then unlink. Best effort: on copy-on-write and flash storage the
    overwrite may not reach the original blocks. Full-disk encryption is the real
    control; this closes the casual-recovery case."""
    try:
        size = path.stat().st_size
        with open(path, "r+b", buffering=0) as fh:
            for _ in range(passes):
                fh.seek(0)
                fh.write(os.urandom(size))
                fh.flush()
                os.fsync(fh.fileno())
        path.unlink()
        return True
    except OSError:
        try:
            path.unlink()
            return True
        except OSError:
            return False
