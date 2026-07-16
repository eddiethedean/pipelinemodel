# Plugins

Plugins are the extension mechanism that allows Pipelantic to execute
portable pipeline plans on different technologies without changing pipeline
definitions.

The core Pipelantic library is intentionally small. It models, validates,
plans, generates contracts, and loads contracts. Plugins provide concrete
runtime behavior.

## Goals

Plugins should:

- Preserve pipeline semantics.
- Be independently installable.
- Support multiple execution technologies.
- Be discoverable.
- Be strongly typed.
- Remain loosely coupled to the core.

## Philosophy

Pipelantic defines **what** a pipeline means.

Plugins define **how** that meaning is realized.

```text
Pipelantic Core
        │
        ▼
Plugin Interface
        │
        ├── Local Execution
        ├── Polars
        ├── Pandas
        ├── Airflow
        ├── Dagster
        ├── Prefect
        ├── Spark
        └── Future Plugins
```

## Plugin Categories

Pipelantic may support several plugin types.

### Execution Plugins

Execute Pipeline Plans.

Examples:

- Local Python
- Airflow
- Dagster
- Prefect

### Dataframe Plugins

Implement DTCS transformations using dataframe engines.

Examples:

- Polars
- Pandas
- DuckDB
- Spark

### Source Plugins

Read data from external systems.

Examples:

- CSV
- Parquet
- PostgreSQL
- S3
- Kafka
- REST APIs

### Sink Plugins

Publish data to external systems.

Examples:

- SQL
- Delta Lake
- Object Storage
- Message Queues
- HTTP Services

### Registry Plugins

Resolve and publish contracts.

Examples:

- Local filesystem
- Git
- Organization registries

## Plugin Discovery

Plugins should be discoverable automatically through Python packaging.

Conceptually:

```python
plugins = PluginRegistry.discover()
```

The exact discovery mechanism is an implementation detail.

## Capabilities

Every plugin should declare its capabilities.

Examples:

- Async support
- Streaming support
- Parallel execution
- Retry support
- Checkpoints
- Transactions
- Batch execution

Planning compares required capabilities against those provided by installed
plugins.

## Selection

Profiles determine which plugins are used.

```python
production = Profile(
    orchestrator="airflow",
    dataframe_engine="polars",
)
```

Changing the profile changes plugin selection—not the pipeline.

## Lifecycle

Typical lifecycle:

```text
Discover
    │
    ▼
Validate
    │
    ▼
Register
    │
    ▼
Capability Evaluation
    │
    ▼
Planning
    │
    ▼
Execution
```

## Versioning

Plugins should publish:

- Plugin name
- Version
- Supported Pipelantic version
- Supported ODCS version
- Supported DTCS version
- Supported DPCS version
- Capability metadata

Planning should reject incompatible plugins.

## Best Practices

- Keep plugins focused.
- Preserve pipeline semantics.
- Declare capabilities explicitly.
- Avoid hidden side effects.
- Fail clearly when requirements cannot be met.

## Anti-Patterns

Avoid:

- Embedding plugin logic into Pipelantic core.
- Changing pipeline semantics.
- Relying on global mutable state.
- Silently ignoring unsupported capabilities.

## Key Principle

> Pipelantic provides the portable modeling framework. Plugins provide the
runtime-specific behavior needed to execute, integrate, and extend that model
without altering its meaning.

## Next Step

Continue with [Resource Providers](RESOURCE_PLUGINS.md) to learn how plugins
acquire and manage runtime resources during execution.
