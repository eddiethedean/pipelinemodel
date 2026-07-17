"""Entry-point discovery for orchestrator plugins."""

from __future__ import annotations

import logging
import warnings
from importlib.metadata import entry_points
from typing import Any

from etlantic.orchestration.protocol import OrchestratorPlugin
from etlantic.registry import PluginDescriptor, RegistryBundle

ORCHESTRATOR_PLUGIN_ENTRY_POINT = "etlantic.orchestrator_plugins"
_LOG = logging.getLogger(__name__)


def _iter_entry_points(group: str) -> Any:
    try:
        return entry_points(group=group)
    except TypeError:  # pragma: no cover
        return entry_points().get(group, [])  # type: ignore[attr-defined]


def discover_orchestrator_plugins() -> dict[str, OrchestratorPlugin]:
    """Load orchestrator plugins registered under the entry-point group."""
    found: dict[str, OrchestratorPlugin] = {}
    for ep in _iter_entry_points(ORCHESTRATOR_PLUGIN_ENTRY_POINT):
        try:
            factory = ep.load()
            plugin = factory() if callable(factory) else factory
            engine = getattr(getattr(plugin, "info", None), "engine", None) or ep.name
            found[str(engine)] = plugin
        except Exception as exc:
            msg = f"Failed to load orchestrator plugin entry point {ep.name!r}: {exc}"
            _LOG.warning(msg)
            warnings.warn(msg, RuntimeWarning, stacklevel=2)
            continue
    return found


def register_discovered_plugins(
    registry: RegistryBundle,
    *,
    plugins: dict[str, OrchestratorPlugin] | None = None,
) -> dict[str, OrchestratorPlugin]:
    """Register discovered orchestrator plugins into a planning registry."""
    discovered = plugins if plugins is not None else discover_orchestrator_plugins()
    for engine, plugin in discovered.items():
        info = plugin.info
        caps = info.capabilities or plugin.capabilities()
        registry.register_plugin(
            PluginDescriptor(
                name=info.name,
                kind="orchestrator",
                version=info.version,
                engine=info.engine or engine,
                capabilities=caps,
                metadata={"protocol_version": info.protocol_version},
            )
        )
    return discovered


def load_orchestrator_plugin(engine: str = "airflow") -> OrchestratorPlugin | None:
    """Return a discovered orchestrator plugin for ``engine``, or None."""
    return discover_orchestrator_plugins().get(engine)


def plugin_registry_snapshot() -> list[dict[str, Any]]:
    """Return serializable descriptors for discovered orchestrator plugins."""
    return [
        plugin.info.to_dict() for plugin in discover_orchestrator_plugins().values()
    ]
