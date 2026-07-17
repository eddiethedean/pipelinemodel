"""Thin Airflow operator callable that coordinates ETLantic step execution."""

from __future__ import annotations

from typing import Any

from etlantic.orchestration.artifacts import xcom_safe_payload
from etlantic.plan.artifacts import ArtifactRef, ArtifactStrategy


def etlantic_step(
    *,
    plan_id: str,
    pipeline_id: str,
    node_name: str,
    node_kind: str,
    artifact_outputs: list[dict[str, Any]] | None = None,
    write_intent: str | None = None,
    retry_policy: str | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Execute one logical ETLantic step inside an Airflow worker.

    The 0.8 reference operator returns artifact-ref XCom payloads only. Full
    in-process engine execution is available via the local orchestrator; Airflow
    workers should resolve durable bindings and invoke the same engines.
    """
    _ = (plan_id, pipeline_id, node_kind, write_intent, retry_policy)
    refs: list[dict[str, Any]] = []
    for raw in artifact_outputs or []:
        try:
            ref = ArtifactRef.from_dict(raw)
        except Exception:
            ref = ArtifactRef(
                identity=str(raw.get("identity") or f"artifact:{node_name}"),
                logical_output=str(raw.get("logical_output") or node_name),
                strategy=ArtifactStrategy(
                    str(raw.get("strategy") or ArtifactStrategy.DURABLE.value)
                ),
            )
        refs.append(xcom_safe_payload(ref))
    if not refs:
        # Always return a durable placeholder ref — never inline row payloads.
        refs.append(
            xcom_safe_payload(
                ArtifactRef(
                    identity=f"artifact:default/{pipeline_id}/{node_name}.result",
                    logical_output=f"{node_name}.result",
                    strategy=ArtifactStrategy.DURABLE,
                )
            )
        )
    return {
        "node_name": node_name,
        "status": "succeeded",
        "xcom": refs,
        "transport": "artifact_ref",
    }
