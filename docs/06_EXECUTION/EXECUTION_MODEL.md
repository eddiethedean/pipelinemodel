# Execution Model

The Execution Model defines how a validated **Pipeline Plan** is realized by an
execution backend.

PipelineModel itself does not execute pipelines. Instead, it produces an
implementation-independent Pipeline Plan that is consumed by an execution
plugin. Every execution backend—from local Python to Airflow—follows the same
logical execution model.

## Goals

The execution model should:

- Preserve pipeline semantics.
- Remain independent of execution technology.
- Support synchronous and asynchronous execution.
- Be deterministic.
- Support multiple runtimes through plugins.
- Keep execution concerns separate from modeling.

## Lifecycle

```text
Pipeline
    │
    ▼
Validation
    │
    ▼
Planning
    │
    ▼
Pipeline Plan
    │
    ▼
Execution Model
    │
    ▼
Execution Plugin
    │
    ▼
Runtime
```

The execution model is the contract between planning and runtime.

## Responsibilities

PipelineModel is responsible for:

- Producing a valid Pipeline Plan
- Preserving ODCS, DTCS, and DPCS semantics
- Selecting implementations
- Resolving bindings
- Producing execution diagnostics

Execution plugins are responsible for:

- Reading sources
- Invoking implementations
- Managing concurrency
- Writing sinks
- Allocating runtime resources
- Reporting execution events

## Execution Units

A Pipeline Plan is executed as a collection of typed steps.

Each step contains:

- Stable identity
- Input bindings
- Output bindings
- Selected implementation
- Parameters
- Dependency information

Steps execute only after all required dependencies have completed successfully.

## Dependency Resolution

Execution order is derived from the Pipeline Plan graph.

Independent branches may execute concurrently when supported by the selected
runtime.

Execution plugins must preserve dependency semantics even if they optimize
execution.

## Sync and Async

Execution plugins must support both synchronous (`def`) and asynchronous
(`async def`) implementations.

PipelineModel normalizes invocation so pipeline authors use a consistent API.

## Resources

Execution uses resources resolved during planning, including:

- Sources
- Sinks
- Database connections
- Object storage
- Secret providers
- Network clients

Resource acquisition is an execution concern rather than a modeling concern.

## Failure Model

Execution plugins preserve the failure semantics established during planning.

Typical actions include:

- Fail
- Retry
- Skip
- Quarantine
- Compensation
- Callback invocation

The chosen backend performs the work but must not change the declared behavior.

## Observability

Execution should expose structured events such as:

- Pipeline started
- Step started
- Step completed
- Step failed
- Retry
- Pipeline completed

Events should reference stable pipeline and step identities.

## Local vs. Remote

The execution model is identical whether work runs:

- In-process
- On another machine
- Inside an orchestrator
- In a distributed cluster

Only the execution plugin changes.

## Best Practices

- Execute only validated Pipeline Plans.
- Preserve graph semantics.
- Respect declared dependencies.
- Keep runtime concerns out of contracts.
- Emit structured diagnostics.

## Anti-Patterns

Avoid:

- Executing Python pipeline definitions directly.
- Re-planning during execution.
- Ignoring declared dependencies.
- Allowing runtime optimizations to alter observable semantics.

## Key Principle

> The Execution Model defines **how a Pipeline Plan is realized**, while
PipelineModel defines **what the pipeline means**. Execution plugins bridge
those two worlds without changing pipeline semantics.

## Next Step

Continue with **EXECUTION_PLUGINS.md** to learn how runtimes implement the
execution model.
