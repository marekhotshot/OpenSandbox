"""Legacy root AMOF package guardrail.

Canonical AMOF Python package lives at `repos/amof/scripts/amof`.
Importing `amof` from root `scripts/amof` is forbidden by default
because it creates a split-brain implementation lane.

Set AMOF_ALLOW_LEGACY_ROOT_AMOF_PACKAGE=1 only for forensic recovery.
"""

from __future__ import annotations

import os

if os.environ.get("AMOF_ALLOW_LEGACY_ROOT_AMOF_PACKAGE") != "1":
    raise RuntimeError(
        "AMOF topology guardrail: root scripts/amof is non-canonical. "
        "Use repos/amof/scripts on PYTHONPATH or run scripts/amof.py, "
        "which delegates to repos/amof/scripts/amof.py. "
        "Set AMOF_ALLOW_LEGACY_ROOT_AMOF_PACKAGE=1 only for forensic recovery."
    )

__version__ = "legacy-root-disabled"
