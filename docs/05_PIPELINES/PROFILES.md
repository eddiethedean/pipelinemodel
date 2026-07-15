# Profiles

A **Profile** defines how a validated Pipeline Plan is bound to a specific
execution environment.

Profiles supply environment-specific configuration without changing the logical
meaning of a pipeline. They bridge the gap between portable pipeline contracts
and concrete runtime infrastructure.

PipelineModel separates **what a pipeline does** from **how and where it
executes**.

## Goals

Profiles should:

- Keep pipelines environment-independent.
- Bind logical resources to physical resources.
- Select execution implementations.
- Configure runtime behavior.
- Support multiple deployment environments.
- Preserve pipeline semantics.

## Philosophy

A pipeline should execute in different environments without modification.

```text
CustomerPipeline
        │
        ├── Development Profile
        ├── Testing Profile
        ├── Staging Profile
        └── Production Profile
```

Each profile produces a different execution plan while preserving identical
logical behavior.

## What a Profile Defines

A profile may define:

- Execution engine
- Orchestrator
- Dataframe backend
- Resource bindings
- Source bindings
- Sink bindings
- Secret providers
- Validation mode
- Logging configuration
- Retry policies
- Concurrency limits
- Timeouts
- Deployment metadata

Profiles never redefine pipeline contracts.

## Example

```python
from pipelinemodel import Profile

production = Profile(
    name="production",
    orchestrator="airflow",
    dataframe_engine="polars",
)
```

Planning uses the selected profile when generating a Pipeline Plan.

## Resource Bindings

Profiles resolve logical bindings into physical resources.

Pipeline:

```python
customers = Source[Customer](
    binding="customers",
)
```

Development profile:

```text
customers -> ./data/customers.csv
```

Production profile:

```text
customers -> warehouse.customer_table
```

The pipeline definition remains unchanged.

## Implementation Selection

Profiles choose execution implementations.

```text
NormalizeCustomers
        │
        ▼
polars implementation
```

A different profile might instead select:

- pandas
- spark
- duckdb
- remote service

The transformation contract does not change.

## Orchestrator Selection

Profiles determine where Pipeline Plans execute.

Examples include:

- Local Python
- Airflow
- Dagster
- Prefect
- Future orchestrators

Planning verifies that the selected orchestrator satisfies all mandatory
pipeline capabilities.

## Validation Configuration

Profiles may configure validation behavior.

Examples:

- Strict validation
- Warning thresholds
- Contract registry resolution
- Compatibility enforcement

These settings influence planning but never alter pipeline semantics.

## Secrets

Profiles reference external secret providers.

Examples:

- Environment variables
- Cloud secret managers
- Vault systems
- Organization-specific providers

Secrets should never be embedded in pipeline contracts or generated DPCS
artifacts.

## Environment Overrides

Profiles may override operational values such as:

- Batch size
- Parallelism
- Retry counts
- Timeouts
- Logging destinations

Overrides should affect runtime behavior only.

## Relationship to Planning

Planning combines:

- Pipeline
- Contracts
- Profile
- Plugin registry

to generate a Pipeline Plan.

Changing profiles should change the execution plan—not the pipeline itself.

## Relationship to DPCS

Profiles are not part of the portable pipeline contract.

DPCS records execution requirements.

Profiles provide environment-specific bindings that satisfy those requirements.

## Best Practices

- Keep profiles small and focused.
- Store secrets externally.
- Use stable logical bindings.
- Maintain separate profiles for development and production.
- Validate profiles before planning.

## Anti-Patterns

Avoid:

- Embedding credentials in profiles.
- Encoding business logic in profiles.
- Modifying pipeline contracts through profile configuration.
- Creating orchestrator-specific pipeline definitions.

## Key Principle

> A Profile describes **where and how** a pipeline executes. A Pipeline
describes **what** the workflow means. Profiles bind pipelines to environments
without changing their semantics.

## Next Step

Continue with **GENERATION.md** to learn how PipelineModel generates portable
artifacts such as DPCS contracts, documentation, diagrams, and execution plans.
