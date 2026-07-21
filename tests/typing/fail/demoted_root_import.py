"""Negative typing fixture: demoted root symbols should not be treated as curated.

This file is intended for a future pyright fail-suite. It documents that
specialist helpers like ``col`` are owned by ``etlantic.sql``, not the root
facade. Until CI enforces ``tests/typing/fail``, keep this as a documentation
anchor only.
"""

from __future__ import annotations

# pyright: reportMissingImports=false
# Intentionally incorrect for a fail fixture: prefer etl.sql.col / from etlantic.sql import col
from etlantic import col  # type: ignore[attr-defined]

_ = col
