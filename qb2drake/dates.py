"""Date parsing shared by every reader.

QuickBooks renders dates differently depending on the export path and the
workstation's regional settings, so we try a spread of formats rather than
assuming one.
"""

from __future__ import annotations

import datetime as _dt
import re
from typing import Optional

DATE_FORMATS = (
    "%m/%d/%Y", "%m/%d/%y",
    "%Y-%m-%d", "%m-%d-%Y", "%m-%d-%y",
    "%b %d, %Y", "%B %d, %Y", "%b %d, %y",
    "%d %b %Y", "%d-%b-%Y", "%d-%b-%y",
    "%Y/%m/%d",
)

_AS_OF = re.compile(
    r"(?:as of|through|ending|period ending)\s+(.+)$", re.IGNORECASE
)


def parse_date(value) -> Optional[_dt.date]:
    if isinstance(value, _dt.datetime):
        return value.date()
    if isinstance(value, _dt.date):
        return value

    text = (value or "").strip()
    if not text:
        return None
    # Excel round-trips dates as "2024-01-05 00:00:00".
    if " 00:00:00" in text:
        text = text.split(" ")[0]
    for fmt in DATE_FORMATS:
        try:
            return _dt.datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def find_report_date(rows, limit: int = 12) -> Optional[_dt.date]:
    """Pull an 'As of <date>' from a report's title block, if present."""
    for row in rows[:limit]:
        for cell in row:
            if not cell:
                continue
            match = _AS_OF.search(cell)
            if match:
                found = parse_date(match.group(1).strip())
                if found:
                    return found
            found = parse_date(cell)
            if found:
                return found
    return None
