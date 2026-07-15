# Execution

Execution is the final stage of the PipelineModel lifecycle.

After a pipeline has been modeled, validated, and planned, an execution plugin
realizes the resulting **Pipeline Plan** using a specific runtime such as local
Python, Polars, Airflow, Dagster, Prefect, or another supported backend.

PipelineModel intentionally separates execution from modeling. The core library
never embeds execution semantics into contracts or pipeline definitions.

## What This Section Covers

This section explains how to:

- Execute Pipeline Plans
- Build execution plugins
- Select execution engines
- Support synchronous and asynchronous execution
- Manage resources
- Handle retries and failures
- Integrate callbacks
- Report diagnostics
- Preserve pipeline semantics across runtimes

## Execution Lifecycle

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
Execution Plugin
    │
    ▼
Runtime
```

Execution plugins consume Pipeline Plans—they do not interpret Python pipeline
definitions directly.

## Core Philosophy

PipelineModel owns:

- Modeling
- Validation
- Planning
- Contract generation
- Contract loading

Execution plugins own:

- Reading data
- Writing data
- Running transformations
- Scheduling work
- Managing concurrency
- Resource allocation
- Runtime integration

This separation allows the same pipeline to execute on multiple runtimes while
preserving identical observable semantics.

## Supported Execution Models

PipelineModel is designed to support:

- Local execution
- Batch execution
- Distributed execution
- Orchestrated workflows
- Streaming execution
- Hybrid execution
- Remote execution

Execution engines may vary, but the Pipeline Plan remains the same.

## Relationship to Standards

Execution is informed by all three standards:

- **ODCS** validates data.
- **DTCS** defines transformation semantics.
- **DPCS** defines pipeline semantics.

Execution plugins preserve these semantics while mapping them onto runtime
capabilities.

## Documentation Roadmap

Read this section in the following order:

1. EXECUTION_ENGINE.md
2. EXECUTION_PLUGINS.md
3. EXECUTION_CONTEXT.md
4. RESOURCE_BINDINGS.md
5. CALLBACK_EXECUTION.md
6. ERROR_HANDLING.md
7. RETRIES.md
8. OBSERVABILITY.md
9. LOCAL_EXECUTION.md

## Key Principles

- Execution follows planning.
- Plugins execute plans, not Python models.
- Contracts remain runtime-independent.
- Execution engines preserve DPCS semantics.
- Modeling and execution evolve independently.

## Next Step

Continue with **EXECUTION_ENGINE.md** to learn how PipelineModel defines the
execution interface that all runtime plugins implement.
