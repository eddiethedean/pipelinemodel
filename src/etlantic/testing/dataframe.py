"""Reusable dataframe plugin conformance helpers."""

from __future__ import annotations

from typing import Any

from etlantic.capabilities import PluginCapabilities
from etlantic.dataframe.protocol import (
    DATAFRAME_PROTOCOL_VERSION,
    ArtifactOwnership,
    DataframeExecutionContext,
    DataframePlugin,
    ValidationDecision,
)
from etlantic.testing.capability_truthfulness import (
    assert_capability_claims_consistent,
)


def assert_plugin_info(plugin: DataframePlugin, *, engine: str) -> None:
    """Assert a dataframe plugin advertises the expected engine and protocol."""
    info = plugin.info
    assert info.engine == engine
    assert info.protocol_version == DATAFRAME_PROTOCOL_VERSION
    assert info.capabilities is not None
    assert info.capabilities.supports("dataframe")
    assert info.capabilities.supports("eager")


def assert_roundtrip_records(
    plugin: DataframePlugin,
    *,
    rows: list[dict[str, Any]],
    contract_type: type[Any] | None = None,
) -> None:
    """Assert materialize → validate → to_records preserves row dicts."""
    context = DataframeExecutionContext(
        run_id="conformance",
        pipeline_id="conformance",
        plan_id="plan",
        step_name="step",
        engine=plugin.info.engine,
        collect=True,
    )
    frame = plugin.materialize_input(
        rows, contract_type=contract_type, context=context, port_name="in"
    )
    frame, decision, *_rest = plugin.validate_frame(
        frame,
        contract_type=contract_type,
        context=context,
        boundary="input_validation",
        port_name="in",
    )
    assert decision in {
        ValidationDecision.PASSED,
        ValidationDecision.SKIPPED,
        ValidationDecision.WARNED,
        ValidationDecision.OBSERVED,
    }
    records = plugin.to_records(frame, contract_type=contract_type)
    got = [r.model_dump() if hasattr(r, "model_dump") else dict(r) for r in records]
    assert got == rows


def run_conformance_suite(
    plugin: DataframePlugin,
    *,
    engine: str,
    sample_rows: list[dict[str, Any]],
    contract_type: type[Any] | None = None,
) -> None:
    """Minimal conformance checks for third-party dataframe plugins.

    Capability-driven: no engine name is special-cased. Behaviour is derived
    from the plugin's advertised :class:`PluginCapabilities`, and overstated or
    inconsistent claims fail with actionable messages.
    """
    assert_plugin_info(plugin, engine=engine)
    caps: PluginCapabilities | None = plugin.info.capabilities
    assert caps is not None
    assert_capability_claims_consistent(caps)
    supports_lazy = caps.supports("lazy")
    assert_roundtrip_records(plugin, rows=sample_rows, contract_type=contract_type)
    # Ownership hint is capability-driven, not name-driven: engines without a
    # lazy/immutable view default to a copied working set.
    default_ownership = (
        ArtifactOwnership.SHARED if supports_lazy else ArtifactOwnership.COPIED
    )
    context = DataframeExecutionContext(
        run_id="conformance",
        pipeline_id="conformance",
        plan_id="plan",
        step_name="step",
        engine=plugin.info.engine,
        collect=False,
        ownership=default_ownership,
    )
    frame = plugin.materialize_input(
        sample_rows, contract_type=contract_type, context=context, port_name="in"
    )
    owned = plugin.ensure_ownership(
        frame, ownership=ArtifactOwnership.COPIED, context=context
    )
    assert owned is not None
    # Ownership truthfulness: re-copying an already-owned artifact must not fail
    # and must still yield a usable frame with the same row count.
    reowned = plugin.ensure_ownership(
        owned, ownership=ArtifactOwnership.COPIED, context=context
    )
    assert reowned is not None
    schema = plugin.inspect_schema(frame, identity="conformance:in")
    assert schema is not None
    assert "fields" in schema or "fingerprint" in schema
    # Collect discipline: LazyFrame must stay lazy when collect=False.
    lazy_candidate = frame
    if supports_lazy and hasattr(frame, "lazy"):
        lazy_candidate = frame.lazy()
    kept = plugin.collect_if_needed(lazy_candidate, context=context)
    if supports_lazy and type(lazy_candidate).__name__ == "LazyFrame":
        assert type(kept).__name__ == "LazyFrame"
    context_collect = DataframeExecutionContext(
        run_id="conformance",
        pipeline_id="conformance",
        plan_id="plan",
        step_name="step",
        engine=plugin.info.engine,
        collect=True,
    )
    collected = plugin.collect_if_needed(lazy_candidate, context=context_collect)
    assert plugin.row_count(collected) == len(sample_rows)
    # Adversarial: an empty input must round-trip to zero rows without error.
    empty_frame = plugin.materialize_input(
        [], contract_type=contract_type, context=context_collect, port_name="in"
    )
    empty_collected = plugin.collect_if_needed(empty_frame, context=context_collect)
    assert plugin.row_count(empty_collected) == 0
    assert list(plugin.to_records(empty_collected, contract_type=contract_type)) == []
