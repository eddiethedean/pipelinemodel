"""Engine registry golden tests."""

from __future__ import annotations

from etlantic.engines import get_engine_registry
from etlantic.profile import Profile


def test_primary_engine_priority_spark_over_sql() -> None:
    registry = get_engine_registry()
    profile = Profile(
        name="mixed",
        spark_engine="pyspark",
        sql_engine="sql",
        dataframe_engine="polars",
    )
    assert registry.primary_engine(profile) == "pyspark"
    assert registry.primary_engine_field(profile) == "spark_engine"


def test_primary_engine_sql_over_dataframe() -> None:
    registry = get_engine_registry()
    profile = Profile(name="sql", sql_engine="sql", dataframe_engine="polars")
    assert registry.primary_engine(profile) == "sql"


def test_primary_engine_defaults_to_dataframe() -> None:
    registry = get_engine_registry()
    profile = Profile(name="local", dataframe_engine="local")
    assert registry.primary_engine(profile) == "local"


def test_is_dataframe_engine_aliases() -> None:
    registry = get_engine_registry()
    assert registry.is_dataframe_engine("polars")
    assert registry.is_dataframe_engine("pandas")
    assert not registry.is_dataframe_engine("sql")
