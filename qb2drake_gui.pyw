"""Double-clickable launcher for the converter.

Saved as .pyw so Windows runs it without opening a console window. Works from
a source checkout without installing anything.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from qb2drake.app import main

if __name__ == "__main__":
    raise SystemExit(main())
