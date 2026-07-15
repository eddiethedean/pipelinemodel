# Plugin SDK

The Plugin SDK enables developers to extend PipelineModel with new execution
engines, dataframe backends, storage providers, resource providers,
orchestration platforms, registries, and future extension points.

PipelineModel is intentionally designed around a small, stable core and a rich
plugin ecosystem. The SDK defines the public interfaces, lifecycle, and
conformance requirements for building those plugins.

## What This Section Covers

This section explains how to:

- Build plugins
- Register plugins
- Declare capabilities
- Implement execution interfaces
- Extend PipelineModel safely
- Test plugins
- Version plugins
- Publish plugins
- Maintain compatibility

## Philosophy

PipelineModel defines the portable modeling layer.

Plugins provide implementation-specific behavior.

```text
        PipelineModel Core
                │
                ▼
            Plugin SDK
                │
     ┌──────────┼──────────┐
     ▼          ▼          ▼
 Execution  Dataframe   Storage
  Plugins     Plugins    Plugins
     │          │          │
     └──────┬───┴──────┬───┘
            ▼          ▼
      Resource     Registry
       Plugins      Plugins
                │
                ▼
       Orchestration Plugins
```

The SDK allows the ecosystem to grow without expanding the responsibilities of
the core library.

## Design Goals

The Plugin SDK should:

- Keep the core framework small.
- Provide stable extension interfaces.
- Preserve PipelineModel semantics.
- Support independent plugin releases.
- Encourage interoperability.
- Enable community-developed plugins.

## Plugin Lifecycle

Typical lifecycle:

1. Discover
2. Register
3. Validate
4. Advertise capabilities
5. Participate in planning
6. Execute or provide services
7. Report diagnostics
8. Clean up resources

## Plugin Categories

The SDK supports plugin categories such as:

- Execution plugins
- Dataframe plugins
- Orchestration plugins
- Storage plugins
- Resource plugins
- Registry plugins
- Future extension types

Each category has its own specialized interface while sharing common lifecycle
and capability concepts.

## Capability-Driven Architecture

Plugins explicitly advertise the features they support.

Planning uses these capabilities to determine whether a plugin can satisfy a
Pipeline Plan without changing its semantics.

## Versioning

Plugins should declare compatibility with:

- PipelineModel
- ODCS
- DTCS
- DPCS

Independent versioning allows plugins to evolve without forcing synchronized
releases across the ecosystem.

## Documentation Roadmap

Read this section in the following order:

1. PLUGIN_ARCHITECTURE.md
2. PLUGIN_LIFECYCLE.md
3. CAPABILITIES.md
4. EXECUTION_PLUGIN_API.md
5. DATAFRAME_PLUGIN_API.md
6. STORAGE_PLUGIN_API.md
7. RESOURCE_PLUGIN_API.md
8. ORCHESTRATION_PLUGIN_API.md
9. REGISTRY_PLUGIN_API.md
10. TESTING.md
11. VERSIONING.md
12. PUBLISHING.md

## Key Principles

- The core owns modeling.
- Plugins own implementation.
- Capability matching drives planning.
- Plugins preserve, not redefine, pipeline semantics.
- Stable SDK interfaces encourage a healthy ecosystem.

## Next Step

Continue with **PLUGIN_ARCHITECTURE.md** to learn the foundational design of the
PipelineModel Plugin SDK.
