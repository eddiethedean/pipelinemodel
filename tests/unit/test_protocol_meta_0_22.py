"""WP4: typed interoperability metadata for protocol context/artifact boundaries."""

from __future__ import annotations

import pytest

from etlantic.protocol_meta import (
    CompileArtifactMeta,
    ExecutionContextMeta,
    ExtensionMetadata,
    coerce_compile_meta,
    coerce_context_meta,
)


def test_coerce_context_meta_none_is_empty() -> None:
    meta = coerce_context_meta(None)
    assert isinstance(meta, ExecutionContextMeta)
    assert meta.engine is None
    assert meta.protocol_version is None
    assert meta.vocabulary_version is None
    assert meta.extensions == {}


def test_coerce_context_meta_extracts_known_fields() -> None:
    meta = coerce_context_meta(
        {
            "engine": "polars",
            "protocol_version": "etlantic.dataframe/1",
            "vocabulary_version": "etlantic.capabilities/1",
        }
    )
    assert meta.engine == "polars"
    assert meta.protocol_version == "etlantic.dataframe/1"
    assert meta.vocabulary_version == "etlantic.capabilities/1"
    assert meta.extensions == {}


def test_coerce_context_meta_namespaced_extensions_pass() -> None:
    meta = coerce_context_meta(
        {"engine": "polars", "etlantic.trace": "abc", "plugin:echo": {"n": 1}}
    )
    assert meta.engine == "polars"
    assert meta.extensions == {"etlantic.trace": "abc", "plugin:echo": {"n": 1}}


def test_coerce_context_meta_bare_extension_key_raises() -> None:
    with pytest.raises(ValueError):
        coerce_context_meta({"engine": "polars", "trace": "abc"})


def test_coerce_context_meta_is_idempotent() -> None:
    original = coerce_context_meta({"engine": "polars"})
    assert coerce_context_meta(original) is original


def test_coerce_context_meta_explicit_extensions_bag() -> None:
    meta = coerce_context_meta({"extensions": {"etlantic.k": "v"}})
    assert meta.extensions == {"etlantic.k": "v"}


def test_coerce_compile_meta_matches_context_semantics() -> None:
    meta = coerce_compile_meta(
        {"engine": "duckdb", "protocol_version": "etlantic.sql/1"}
    )
    assert isinstance(meta, CompileArtifactMeta)
    assert meta.engine == "duckdb"
    assert meta.protocol_version == "etlantic.sql/1"


def test_extension_metadata_mapping_protocol() -> None:
    bag = ExtensionMetadata(root={"etlantic.a": 1, "plugin:b": 2})
    assert len(bag) == 2
    assert "etlantic.a" in bag
    assert bag["etlantic.a"] == 1
    assert bag.get("missing", "default") == "default"
    assert set(bag.keys()) == {"etlantic.a", "plugin:b"}
    assert bag.to_dict() == {"etlantic.a": 1, "plugin:b": 2}
    assert sorted(bag) == ["etlantic.a", "plugin:b"]


def test_extension_metadata_rejects_bare_keys() -> None:
    with pytest.raises(ValueError):
        ExtensionMetadata(root={"bare": 1})


def test_dataframe_context_meta_accessor() -> None:
    from etlantic.dataframe.protocol import DataframeExecutionContext

    ctx = DataframeExecutionContext(
        run_id="r",
        pipeline_id="p",
        plan_id="pl",
        step_name="s",
        engine="polars",
        metadata={"engine": "polars", "etlantic.trace": "t"},
    )
    meta = ctx.context_meta
    assert isinstance(meta, ExecutionContextMeta)
    assert meta.engine == "polars"
    assert meta.extensions == {"etlantic.trace": "t"}


def test_sql_compiled_artifact_meta_accessor() -> None:
    from etlantic.sql.protocol import CompiledSql

    compiled = CompiledSql(
        statement_id="s1",
        text="SELECT 1",
        metadata={"engine": "duckdb", "protocol_version": "etlantic.sql/1"},
    )
    meta = compiled.artifact_meta
    assert isinstance(meta, CompileArtifactMeta)
    assert meta.engine == "duckdb"
    assert meta.protocol_version == "etlantic.sql/1"
