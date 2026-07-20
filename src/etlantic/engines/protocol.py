"""Engine family protocol for centralized classification."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from etlantic.profile import Profile


class EngineFamily(Protocol):
    """One execution engine family (local, dataframe, sql, spark)."""

    name: str
    entry_point_group: str | None

    def matches(self, engine: str) -> bool:
        """Return whether ``engine`` belongs to this family."""
        ...

    def default_capabilities(self, profile: Profile) -> list[str]:
        """Default capability requirements for planning."""
        ...
