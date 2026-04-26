#!/usr/bin/env python3
"""Root AMOF CLI wrapper.

Canonical AMOF implementation lives in `repos/amof/scripts/amof.py`.
The root workspace is a wrapper/config/audit surface only. Keeping a
second full CLI implementation in `scripts/amof.py` repeatedly caused
split-brain between root `scripts/amof/...` and `repos/amof/scripts/...`.

This file therefore execs the canonical entrypoint and never imports
the root `scripts/amof` package.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CANONICAL_ENTRYPOINT = ROOT / "repos" / "amof" / "scripts" / "amof.py"


def main() -> None:
    if not CANONICAL_ENTRYPOINT.exists():
        sys.stderr.write(
            "AMOF topology error: canonical entrypoint missing:\n"
            f"  {CANONICAL_ENTRYPOINT}\n"
            "Root scripts/amof.py is a wrapper only and cannot run without repos/amof.\n"
        )
        raise SystemExit(127)

    os.execv(sys.executable, [sys.executable, str(CANONICAL_ENTRYPOINT), *sys.argv[1:]])


if __name__ == "__main__":
    main()
