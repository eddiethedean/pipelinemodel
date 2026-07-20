"""Capability validation phase."""

from __future__ import annotations

from typing import TYPE_CHECKING

from etlantic.diagnostics import Diagnostic, Severity

if TYPE_CHECKING:
    from etlantic.pipeline import Pipeline
    from etlantic.policy import ValidationPolicy
    from etlantic.registry import PlanningContext


def phase_capability(
    pipeline_cls: type[Pipeline],
    context: PlanningContext,
    policy: ValidationPolicy,
) -> list[Diagnostic]:
    from etlantic.capabilities import CapabilityDecision, negotiate_capabilities
    from etlantic.engines import get_engine_registry

    diagnostics: list[Diagnostic] = []
    registry = get_engine_registry()
    profile = context.profile
    engine_name = registry.primary_engine(profile)
    available = context.registry.engines.get(engine_name)
    if available is None:
        diagnostics.append(
            Diagnostic(
                code="PMPLAN401",
                severity=Severity.ERROR,
                message=f"No plugin capabilities registered for engine {engine_name!r}.",
                path=("profile", profile.name, registry.primary_engine_field(profile)),
            )
        )
        return diagnostics

    fallback = None
    if context.fallback_engine:
        fallback = context.registry.engines.get(context.fallback_engine)
    allow_fallback = context.allow_capability_fallback or bool(
        policy.allowed_capability_fallbacks
    )
    negotiations = negotiate_capabilities(
        requirements=context.required_capabilities,
        available=available,
        fallback=fallback,
        allow_fallback=allow_fallback,
    )
    for item in negotiations:
        if item.decision is CapabilityDecision.UNSUPPORTED:
            diagnostics.append(
                Diagnostic(
                    code="PMPLAN402",
                    severity=Severity.ERROR,
                    message=item.message
                    or f"Unsupported capability {item.requirement!r}.",
                    path=("capability", item.requirement),
                    metadata=item.to_dict(),
                )
            )
        elif item.decision is CapabilityDecision.FALLBACK:
            diagnostics.append(
                Diagnostic(
                    code="PMPLAN403",
                    severity=Severity.WARNING,
                    message=item.message
                    or f"Using fallback for capability {item.requirement!r}.",
                    path=("capability", item.requirement),
                    metadata=item.to_dict(),
                )
            )
    return diagnostics
