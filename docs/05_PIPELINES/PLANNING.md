# Planning

Planning is the process of converting a validated `Pipeline` into an implementation-independent
**Pipeline Plan**.

A Pipeline Plan preserves the logical semantics of a pipeline while resolving
its dependencies, bindings, implementations, and execution requirements. It is
the final product of the modeling layer and the starting point for execution
plugins.

Planning is deliberately separated from execution. A pipeline may be planned
many times for different execution environments without changing its logical
definition.

## Goals

Pipeline planning should:

- Preserve pipeline semantics.
- Remain independent of execution engines.
- Produce deterministic results.
- Resolve implementations and bindings.
- Verify execution capabilities.
- Generate a reusable Pipeline Plan.

## Planning Philosophy

PipelineModel follows a staged planning process.

```text
Python Pipeline
       │
       ▼
Validation
       │
       ▼
Pipeline Planner
       │
       ▼
Pipeline Plan
       │
       ▼
Execution Plugin
       │
       ▼
Runtime
```

Execution plugins consume Pipeline Plans rather than Python pipeline classes.

## Inputs

The planner consumes:

- Pipeline definitions
- Data contracts (ODCS)
- Transformation contracts (DTCS)
- Pipeline contracts (DPCS)
- Execution profile
- Plugin registry
- Runtime bindings

## Planning Phases

### 1. Graph Construction

Build the logical DAG.

Produces:

- Nodes
- Edges
- Dependencies
- Public interfaces

### 2. Contract Resolution

Resolve referenced contracts.

Checks:

- ODCS references
- DTCS references
- Nested DPCS references
- Version compatibility

### 3. Binding Resolution

Resolve logical bindings into runtime bindings.

Examples:

- Source bindings
- Sink bindings
- Resource bindings
- Secret references

The logical pipeline remains unchanged.

### 4. Implementation Selection

Choose an implementation for each transformation.

Conceptually:

```python
NormalizeCustomers
    -> "polars"
```

Selection depends on:

- Execution profile
- Available plugins
- Runtime capabilities

### 5. Capability Evaluation

Verify that the selected execution environment supports the required semantics.

Examples:

- Parallel execution
- Retry
- Streaming
- Checkpoints
- Compensation
- Approval workflows

Planning fails if mandatory capabilities are unavailable.

### 6. Plan Generation

Generate a normalized Pipeline Plan suitable for execution.

The Pipeline Plan contains no Python-specific authoring constructs.

## Pipeline Plan

A Pipeline Plan should preserve:

- Pipeline identity
- Graph topology
- Step identities
- Contract references
- Public interfaces
- Parameters
- Execution requirements
- Scheduling intent
- Failure semantics
- Quality gates
- Lineage

Execution plugins must preserve these semantics.

## Multiple Plans

The same pipeline may produce multiple plans.

```text
CustomerPipeline
      │
      ├── Local Plan
      ├── Airflow Plan
      ├── Dagster Plan
      └── Prefect Plan
```

Each plan represents the same logical pipeline.

## Determinism

Planning should be deterministic.

Equivalent inputs should always produce semantically equivalent Pipeline Plans.

Differences should only arise from:

- Different execution profiles
- Different plugin sets
- Different runtime bindings

## Relationship to DPCS

Planning consumes a DPCS-compatible model and produces a normalized execution
plan.

DPCS describes **what the pipeline means**.

The Pipeline Plan describes **how a compatible execution environment should
realize those semantics**.

## Validation vs. Planning

Validation answers:

> Is this pipeline valid?

Planning answers:

> Given a valid pipeline and an execution profile, what is the execution plan?

Planning never repairs an invalid pipeline.

## Diagnostics

Planning failures should return structured diagnostics.

Examples:

- Missing implementation
- Unsatisfied capability
- Unresolved binding
- Missing resource
- Version incompatibility
- Ambiguous implementation

## Planning API

Conceptually:

```python
plan = CustomerPipeline.plan(
    profile="production",
)
```

The returned plan may then be executed by any compatible execution plugin.

## Caching

Pipeline Plans may be cached.

Cached plans remain valid only while:

- Pipeline definition
- Contract versions
- Plugin versions
- Execution profile

remain compatible.

## Best Practices

- Validate before planning.
- Keep planning deterministic.
- Separate planning from execution.
- Resolve implementations during planning.
- Preserve DPCS semantics.

## Anti-Patterns

Avoid:

- Executing transformations during planning.
- Modifying pipeline semantics while planning.
- Depending on orchestrator-specific planners.
- Hiding planning failures until runtime.

## Key Principle

> Planning converts a validated, declarative pipeline into an implementation-independent
> execution plan while preserving every observable semantic defined by the
> pipeline contracts.

## Next Step

Continue with **EXECUTION_PROFILES.md** to learn how execution profiles influence
planning without changing the logical pipeline.
