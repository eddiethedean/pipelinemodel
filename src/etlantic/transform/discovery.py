"""Entry-point discovery for portable transform compilers."""

from __future__ import annotations

import logging
import warnings
from importlib.metadata import entry_points
from typing import Any

from etlantic.registry import PluginDescriptor, RegistryBundle
from etlantic.transform.compiler import PortableTransformCompiler

TRANSFORM_COMPILER_ENTRY_POINT = "etlantic.transform_compilers"
_LOG = logging.getLogger(__name__)


def discover_transform_compilers() -> dict[str, PortableTransformCompiler]:
    """Load compilers registered under ``etlantic.transform_compilers``.

    Returns entry-point name → compiler instance. The entry-point name is the
    stable engine key. Broken entry points are skipped with a warning. Duplicate
    entry-point names fail closed.
    """
    found: dict[str, PortableTransformCompiler] = {}
    try:
        eps = entry_points(group=TRANSFORM_COMPILER_ENTRY_POINT)
    except TypeError:  # pragma: no cover - older importlib API
        eps = entry_points().get(TRANSFORM_COMPILER_ENTRY_POINT, [])  # type: ignore[attr-defined]
    for ep in eps:
        try:
            factory = ep.load()
            compiler = factory() if callable(factory) else factory
            if not isinstance(compiler, PortableTransformCompiler):
                # runtime_checkable Protocol — require info/analyze/compile/execute
                missing = [
                    name
                    for name in ("info", "analyze", "compile", "execute")
                    if not hasattr(compiler, name)
                ]
                if missing:
                    raise TypeError(
                        f"entry point {ep.name!r} does not implement "
                        f"PortableTransformCompiler (missing {missing})"
                    )
            engine_key = str(ep.name)
            if engine_key in found:
                raise RuntimeError(
                    f"Duplicate transform compiler entry point {engine_key!r}; "
                    "entry-point names must be unique stable engine keys."
                )
            info_engine = getattr(getattr(compiler, "info", None), "engine", None)
            if info_engine is not None and str(info_engine) != engine_key:
                warnings.warn(
                    f"Transform compiler entry point {engine_key!r} reports "
                    f"info.engine={info_engine!r}; the entry-point name is the "
                    "stable discovery key.",
                    RuntimeWarning,
                    stacklevel=2,
                )
            found[engine_key] = compiler
        except Exception as exc:
            msg = f"Failed to load transform compiler entry point {ep.name!r}: {exc}"
            _LOG.warning(msg)
            warnings.warn(msg, RuntimeWarning, stacklevel=2)
            continue
    return found


def register_discovered_compilers(
    registry: RegistryBundle,
    *,
    compilers: dict[str, PortableTransformCompiler] | None = None,
) -> dict[str, PortableTransformCompiler]:
    """Register discovered transform compilers into a planning registry."""
    discovered = compilers if compilers is not None else discover_transform_compilers()
    for engine, compiler in discovered.items():
        info = compiler.info
        registry.register_plugin(
            PluginDescriptor(
                name=info.name,
                kind="transform_compiler",
                version=info.version,
                engine=info.engine or engine,
                capabilities=None,
                metadata={
                    "compiler_protocol": info.compiler_protocol,
                    "dtcs_plan_versions": list(info.dtcs_plan_versions),
                    "transform_capabilities": info.capabilities.to_dict(),
                },
            )
        )
    return discovered


def load_transform_compiler(engine: str) -> PortableTransformCompiler | None:
    """Return a discovered compiler for ``engine``, or None.

    This loads the unfiltered discovery set. Prefer
    :func:`discover_transform_compilers_for_profile` on planning and run paths
    so production allowlists cannot be bypassed.
    """
    return discover_transform_compilers().get(engine)


def compiler_registry_snapshot() -> list[dict[str, Any]]:
    """Return serializable descriptors for discovered compilers."""
    return [c.info.to_dict() for c in discover_transform_compilers().values()]


def discover_transform_compilers_for_profile(
    profile: Any | None,
) -> dict[str, PortableTransformCompiler]:
    """Discover compilers and apply ``profile.plugin_allowlist`` trust rules."""
    found = discover_transform_compilers()
    if profile is None:
        return found
    from etlantic.plugin_trust import filter_plugins_by_allowlist

    kept, _diagnostics = filter_plugins_by_allowlist(found, profile)
    return kept
