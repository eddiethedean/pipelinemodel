"""In-memory relation handle used by portable SQL conformance."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SqlRelationFrame:
    """Row-backed relation used as a portable SQL compiler input/output."""

    rows: list[dict[str, Any]] = field(default_factory=list)
    name: str = ""

    def to_dicts(self) -> list[dict[str, Any]]:
        return list(self.rows)

    @property
    def columns(self) -> list[str]:
        if not self.rows:
            return []
        return list(self.rows[0].keys())
