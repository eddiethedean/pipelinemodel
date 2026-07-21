"""Public Spark plugin conformance helpers (etlantic.spark/1).

The suite is session-free: it exercises discovery metadata, capability
truthfulness, and secret-free region compilation. Live-session execution is
covered by backend-specific tests in the plugin package, because it requires a
running ``SparkSession``.
"""

from __future__ import annotations

from etlantic.runtime.logging import redact_message
from etlantic.spark.protocol import (
    SPARK_PROTOCOL_VERSION,
    SparkCompilationContext,
    SparkPlanRegion,
    SparkPlugin,
)
from etlantic.testing.capability_truthfulness import (
    assert_capability_claims_consistent,
)


def assert_spark_plugin_info(plugin: SparkPlugin, *, engine: str = "pyspark") -> None:
    """Assert a Spark plugin advertises the expected engine and protocol."""
    info = plugin.info
    assert info.engine == engine
    assert info.protocol_version == SPARK_PROTOCOL_VERSION
    assert info.capabilities is not None
    caps = plugin.capabilities()
    assert caps is not None
    assert caps.supports("spark") or bool(getattr(caps, "spark", False))
    assert_capability_claims_consistent(caps)
    # info.capabilities and capabilities() must agree on the family root.
    assert info.capabilities.supports("spark") == caps.supports("spark"), (
        "SparkPluginInfo.capabilities and capabilities() disagree on 'spark'."
    )


def run_spark_conformance_suite(
    plugin: SparkPlugin,
    *,
    engine: str = "pyspark",
    binding: str = "conformance_source",
) -> None:
    """Session-free conformance checks for Spark plugins.

    Compiles a trivial region and asserts the compiled artifact is secret-free
    and structurally consistent. Overstated capabilities fail via
    :func:`assert_capability_claims_consistent`.
    """
    assert_spark_plugin_info(plugin, engine=engine)

    dataset = plugin.dataset_from_binding(binding=binding)
    assert dataset is not None

    region = SparkPlanRegion(
        identity="conformance:region",
        node_names=("normalize",),
    )
    ctx = SparkCompilationContext(
        run_id="conformance",
        pipeline_id="conformance",
        plan_id="plan",
        region_id=region.identity,
    )
    compiled = plugin.compile(region, context=ctx)
    assert compiled is not None
    assert compiled.node_names == region.node_names
    # Compiled regions must be secret-free and JSON-inspectable.
    payload = str(compiled.to_dict())
    assert payload == redact_message(payload), (
        "Compiled Spark plan contains secret-like text."
    )
