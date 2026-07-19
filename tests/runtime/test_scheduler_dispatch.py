"""Scheduler discovery and Profile.orchestrator dispatch tests."""

from __future__ import annotations

import pytest

from etlantic.exceptions import ETLanticError
from etlantic.runtime.scheduler import LocalScheduler
from etlantic.runtime.scheduler_discovery import resolve_scheduler


def test_resolve_local_builtin() -> None:
    scheduler = resolve_scheduler("local")
    assert isinstance(scheduler, LocalScheduler)
    assert scheduler.info.name == "local"


def test_resolve_missing_plugin_fails_closed() -> None:
    with pytest.raises(ETLanticError, match="No ExecutionScheduler"):
        resolve_scheduler("prefect", plugins={})


def test_resolve_airflow_rejected() -> None:
    with pytest.raises(ETLanticError, match="compile target"):
        resolve_scheduler("airflow")
