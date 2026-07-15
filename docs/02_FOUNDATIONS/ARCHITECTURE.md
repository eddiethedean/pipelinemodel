# Architecture

## Overview

PipelineModel is a **typed pipeline modeling framework**.

Its responsibility is to model, validate, document, and plan data
pipelines. It intentionally delegates execution to external plugins.

The architecture follows a layered design that cleanly separates
business intent from runtime execution.

``` text
Python Models
      │
      ▼
PipelineModel
      │
      ├── Validation
      ├── Contract Generation
      ├── Documentation
      ├── Visualization
      ├── Planning
      ▼
Execution Plugins
      │
      ▼
Execution Engines
```

The framework owns the logical model.

Plugins own execution.

------------------------------------------------------------------------

# Architectural Layers

``` text
┌────────────────────────────────────┐
│ User Python Code                   │
│                                    │
│ • DataContractModel                │
│ • Transformation                   │
│ • Pipeline                         │
└────────────────────────────────────┘
                │
                ▼
┌────────────────────────────────────┐
│ PipelineModel Core                 │
│                                    │
│ Type Introspection                 │
│ Validation                         │
│ Graph Builder                      │
│ Planning                           │
│ Contract Generation                │
│ Documentation                      │
│ Visualization                      │
└────────────────────────────────────┘
                │
                ▼
┌────────────────────────────────────┐
│ Plugin Layer                       │
│                                    │
│ Dataframe Plugins                  │
│ Orchestrator Plugins               │
│ Storage Plugins                    │
│ Resource Providers                 │
│ Compiler Plugins                   │
└────────────────────────────────────┘
                │
                ▼
┌────────────────────────────────────┐
│ Runtime Technologies               │
│                                    │
│ Polars                             │
│ Pandas                             │
│ Airflow                            │
│ SQLAlchemy                         │
│ DuckDB                             │
│ Cloud Services                     │
└────────────────────────────────────┘
```

------------------------------------------------------------------------

# Core Components

## Data Modeling

Data contracts are authored using ContractModel-compatible Pydantic
models.

Responsibilities:

-   describe datasets
-   validate records
-   generate ODCS
-   provide type information

------------------------------------------------------------------------

## Transformation Modeling

Transformation classes define:

-   inputs
-   outputs
-   parameters
-   metadata

They describe interfaces only.

Execution implementations are registered separately.

------------------------------------------------------------------------

## Pipeline Modeling

Pipeline classes connect transformations together.

Responsibilities include:

-   dependency graph construction
-   type compatibility
-   contract references
-   execution planning

Pipelines describe logical topology rather than runtime behavior.

------------------------------------------------------------------------

## Validation Engine

The validation engine performs static analysis before execution.

Examples include:

-   incompatible contracts
-   missing inputs
-   unused outputs
-   parameter validation
-   plugin compatibility
-   cyclic graphs

Validation should catch as many issues as possible before execution
begins.

------------------------------------------------------------------------

## Contract Generation

PipelineModel generates:

-   ODCS
-   DTCS
-   DPCS

Generated contracts are portable artifacts that can be shared
independently of Python code.

------------------------------------------------------------------------

## Planning Engine

Planning converts a logical pipeline into an execution plan.

Responsibilities include:

-   dependency ordering
-   plugin resolution
-   profile application
-   resource resolution
-   runtime configuration

Planning does not execute work.

------------------------------------------------------------------------

## Plugin Manager

The plugin manager discovers and configures runtime integrations.

Examples:

-   dataframe plugins
-   orchestrators
-   storage systems
-   compilers

The core framework depends only on abstract interfaces.

------------------------------------------------------------------------

# Internal Data Flow

PipelineModel follows a predictable lifecycle.

``` text
Python Classes
        │
        ▼
Type Introspection
        │
        ▼
Logical Pipeline Graph
        │
        ▼
Validation
        │
        ▼
Execution Plan
        │
        ▼
Plugin Dispatch
        │
        ▼
Runtime Execution
```

Every stage produces structured metadata that can be inspected,
documented, or visualized.

------------------------------------------------------------------------

# Runtime Independence

One of PipelineModel's central architectural goals is runtime
independence.

A pipeline should not change simply because execution technology
changes.

``` text
Logical Pipeline

        │

        ├──────────► Polars

        ├──────────► Pandas

        ├──────────► Airflow

        └──────────► Future Plugins
```

Execution bindings belong to profiles and plugins rather than pipeline
definitions.

------------------------------------------------------------------------

# Async Architecture

PipelineModel is asynchronous internally.

Every user callable---whether synchronous or asynchronous---is
normalized through a common invocation layer.

This allows users to write:

``` python
def transform(...):
    ...
```

or

``` python
async def transform(...):
    ...
```

without changing the surrounding pipeline.

The execution engine chooses the appropriate invocation strategy.

------------------------------------------------------------------------

# Generated Artifacts

PipelineModel can derive multiple outputs from the same Python model.

``` text
Python Classes
      │
      ├── ODCS
      ├── DTCS
      ├── DPCS
      ├── Documentation
      ├── Mermaid
      ├── Graphviz
      ├── HTML
      └── Execution Plans
```

The Python model remains the single source of truth.

------------------------------------------------------------------------

# Separation of Responsibilities

  Responsibility             Component
  -------------------------- ----------------------
  Data semantics             ContractModel / ODCS
  Transformation semantics   DTCS
  Pipeline topology          DPCS
  Pipeline modeling          PipelineModel
  Validation                 PipelineModel
  Planning                   PipelineModel
  Documentation              PipelineModel
  Execution                  Plugins
  Scheduling                 Orchestrator Plugins
  Data processing            Dataframe Plugins

This separation allows each component to evolve independently while
maintaining a coherent developer experience.

------------------------------------------------------------------------

# Architectural Principles

PipelineModel follows these architectural rules:

-   Types define interfaces.
-   Contracts define semantics.
-   Pipelines define topology.
-   Plugins define execution.
-   Profiles define runtime bindings.
-   Planning precedes execution.
-   Validation precedes planning.
-   Python remains the source of truth.

------------------------------------------------------------------------

# Looking Ahead

This document provides the conceptual architecture.

Subsequent sections describe the public APIs, plugin interfaces,
execution model, and runtime behavior in greater detail.
