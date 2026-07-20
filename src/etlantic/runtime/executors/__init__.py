"""Runtime engine executor registry (internal refactor surface)."""

from etlantic.runtime.executors.protocol import EngineExecutor
from etlantic.runtime.executors.registry import (
    DataframeExecutor,
    ExecutorRegistry,
    SparkExecutor,
    SqlExecutor,
    get_executor_registry,
)

__all__ = [
    "DataframeExecutor",
    "EngineExecutor",
    "ExecutorRegistry",
    "SparkExecutor",
    "SqlExecutor",
    "get_executor_registry",
]
