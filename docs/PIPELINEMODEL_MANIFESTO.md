# PipelineModel Manifesto

## Data Engineering Deserves a Better Developer Experience

Modern data engineering is powerful, but it is too often fragmented.
Data contracts, transformation logic, orchestration, validation,
documentation, and execution are typically spread across disconnected
tools, frameworks, and handwritten configuration.

PipelineModel exists to unify these concerns without replacing the
execution ecosystem.

PipelineModel is **not** another execution engine.

It is a **modeling framework** for building typed, contract-driven ETL
pipelines.

Execution belongs to the best tool for the job.

## Our Vision

PipelineModel is to data pipelines what FastAPI is to web APIs.

Users should describe **what** a pipeline is using Python type
annotations and declarative classes. PipelineModel should infer
everything else that can be inferred.

The result is a pipeline that is:

-   strongly typed
-   self-documenting
-   contract-driven
-   statically validated
-   portable
-   execution-engine independent

## Core Principles

### Types are the source of truth

Python type annotations define pipeline interfaces.

### Contracts are generated, not hand-written

ODCS, DTCS, and DPCS should be derived from Python models whenever
possible.

### Pipelines model intent

PipelineModel describes logical data flow, not runtime execution.

### Execution is pluggable

Pandas, Polars, SQLAlchemy, Airflow, Dagster, local Python, cloud
services, and future systems are execution plugins---not core framework
concerns.

### Validation comes before execution

Invalid pipelines should fail during planning, not after expensive
execution has begun.

### Async should be effortless

Users may write `def` or `async def`. PipelineModel manages invocation
and concurrency internally.

### FastAPI-inspired developer experience

Type annotations should drive validation, documentation, editor support,
and contract generation with minimal configuration.

### Open standards first

PipelineModel embraces portable specifications through:

-   ODCS (Data Contracts)
-   DTCS (Transformation Contracts)
-   DPCS (Pipeline Contracts)

### Python first

The reference implementation is pure Python, emphasizing readability,
extensibility, and ecosystem compatibility.

### One pipeline, many runtimes

A single pipeline definition should execute through different execution
engines by changing bindings or profiles---not rewriting business logic.

## What PipelineModel Is Not

PipelineModel is not:

-   an orchestration engine
-   a dataframe library
-   a scheduler
-   a workflow server
-   a replacement for Pandas or Polars
-   a replacement for Airflow, Prefect, or Dagster

Instead, it coordinates these systems through a unified typed model.

## Success

PipelineModel succeeds when developers can define data contracts,
transformations, and pipelines with the same confidence and clarity that
FastAPI brought to web APIs.

If a developer can understand a pipeline by reading its Python types,
and confidently execute it on the runtime of their choice, PipelineModel
has achieved its mission.
