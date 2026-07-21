"""0.22 WP1: capability-driven engine identity (no privileged name sets)."""

from __future__ import annotations

from etlantic.capabilities import PluginCapabilities
from etlantic.engines import ExecutionFamily, get_engine_registry
from etlantic.plugins.coordinator import (
    should_discover_dataframe_plugins,
    should_discover_spark_plugins,
    should_discover_sql_plugins,
    should_include_transform_compilers,
)


def test_synthetic_dataframe_capability_via_registry() -> None:
    registry = get_engine_registry()
    engines = {
        "acme_df": PluginCapabilities(engine="acme_df", dataframe=True),
    }
    assert registry.is_dataframe_engine("acme_df", engines)
    assert (
        registry.resolve_execution_family("acme_df", engines)
        is ExecutionFamily.DATAFRAME
    )


def test_builtin_polars_fallback_without_registration() -> None:
    registry = get_engine_registry()
    assert registry.is_dataframe_engine("polars")
    assert registry.is_dataframe_engine("polars", engines={})
    assert registry.resolve_execution_family("polars") is ExecutionFamily.DATAFRAME


def test_unknown_engine_without_capabilities_is_not_dataframe() -> None:
    registry = get_engine_registry()
    assert not registry.is_dataframe_engine("acme_unknown")
    assert not registry.is_dataframe_engine("acme_unknown", engines={})
    assert registry.resolve_execution_family("acme_unknown") is None


def test_discover_planning_predicates_for_third_party_dataframe() -> None:
    assert should_discover_dataframe_plugins("acme_df")
    assert should_include_transform_compilers("acme_df", None)
    assert not should_discover_dataframe_plugins("local")
    assert not should_discover_dataframe_plugins("null")
    assert not should_discover_dataframe_plugins("")


def test_discover_planning_predicates_sql_and_spark() -> None:
    assert should_discover_sql_plugins("sql")
    assert should_discover_sql_plugins("acme_sql")
    assert not should_discover_sql_plugins("local")
    assert not should_discover_sql_plugins(None)

    assert should_discover_spark_plugins("pyspark")
    assert should_discover_spark_plugins("acme_spark")
    assert not should_discover_spark_plugins(None)
    assert should_include_transform_compilers("local", "acme_spark")


def test_capability_backed_spark_and_sql_identity() -> None:
    registry = get_engine_registry()
    engines = {
        "acme_spark": PluginCapabilities(
            engine="acme_spark", dataframe=False, spark=True
        ),
        "acme_sql": PluginCapabilities(engine="acme_sql", dataframe=False, sql=True),
    }
    assert registry.is_spark_engine("acme_spark", engines)
    assert registry.is_sql_engine("acme_sql", engines)
    assert (
        registry.resolve_execution_family("acme_spark", engines)
        is ExecutionFamily.SPARK
    )
    assert registry.resolve_execution_family("acme_sql", engines) is ExecutionFamily.SQL
