"""Execution-family identity derived from capabilities and registration."""

from __future__ import annotations

from enum import StrEnum


class ExecutionFamily(StrEnum):
    """Logical execution family for planning and runtime dispatch.

    Families are resolved from registered descriptors and capabilities.
    First-party engine names are ordinary registered engines, not a
    privileged allowlist.
    """

    LOCAL = "local"
    DATAFRAME = "dataframe"
    SQL = "sql"
    SPARK = "spark"
    ORCHESTRATION = "orchestration"
    TRANSFORM_COMPILER = "transform_compiler"
    SECRET = "secret"
    SCHEDULER = "scheduler"
