#!/usr/bin/env python3
"""Drake Prep Desk entry point. Run `./prepdesk.py --help`."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from drakeprep.cli import main

if __name__ == "__main__":
    sys.exit(main())
