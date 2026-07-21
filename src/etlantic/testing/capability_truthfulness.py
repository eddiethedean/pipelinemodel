"""Capability-truthfulness conformance helpers shared across plugin suites.

Third-party and first-party plugins advertise :class:`PluginCapabilities`.
These helpers assert that advertised claims are internally consistent with the
versioned capability vocabulary (``etlantic.capabilities/1``) and, where a
behaviour probe is supplied, that observed behaviour matches the claim.

Findings are raised as :class:`AssertionError` with actionable, secret-free
messages so overstated capabilities fail closed.
"""

from __future__ import annotations

from collections.abc import Callable

from etlantic.capabilities import (
    CAPABILITY_VOCABULARY_VERSION,
    PluginCapabilities,
    validate_capability_claims,
    vocabulary_major_compatible,
)


def assert_capability_claims_consistent(caps: PluginCapabilities) -> None:
    """Assert advertised capabilities satisfy vocabulary implications/conflicts.

    Raises :class:`AssertionError` listing every inconsistent claim so plugin
    authors get one actionable report instead of a single opaque failure.
    """
    version = getattr(caps, "vocabulary_version", None)
    if version is not None:
        assert vocabulary_major_compatible(version), (
            f"Plugin advertises capability vocabulary {version!r}, which is not "
            f"major-compatible with core {CAPABILITY_VOCABULARY_VERSION!r}."
        )
    findings = validate_capability_claims(caps)
    assert not findings, "Inconsistent capability claims:\n  - " + "\n  - ".join(
        findings
    )


def assert_capability_matches_behavior(
    caps: PluginCapabilities,
    capability: str,
    probe: Callable[[], bool],
    *,
    description: str | None = None,
) -> None:
    """Assert an advertised capability flag matches an observed behaviour probe.

    ``probe`` returns ``True`` when the behaviour is actually present. A plugin
    must not claim a capability it does not exhibit, nor exhibit a capability it
    denies (which would hide behaviour from planning).
    """
    claimed = bool(getattr(caps, capability, False)) or caps.supports(capability)
    observed = bool(probe())
    label = description or capability
    if claimed and not observed:
        raise AssertionError(
            f"Capability {capability!r} is advertised but {label} was not "
            "observed; overstated capabilities must fail conformance."
        )
    if observed and not claimed:
        raise AssertionError(
            f"Behaviour {label} was observed but capability {capability!r} is "
            "not advertised; planning cannot see undeclared behaviour."
        )
