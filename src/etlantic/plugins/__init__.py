"""Shared plugin discovery coordination (internal refactor surface)."""

from etlantic.plugins.coordinator import (
    PluginDiscoveryCoordinator,
    PluginDiscoveryResult,
    profile_plugin_key,
)

__all__ = [
    "PluginDiscoveryCoordinator",
    "PluginDiscoveryResult",
    "profile_plugin_key",
]
