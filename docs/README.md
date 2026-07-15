# PipelineModel Documentation

Welcome to the official documentation for **PipelineModel**.

PipelineModel is a Python framework for building **typed,
contract-driven ETL pipelines**. Inspired by FastAPI, it uses Python
type annotations and declarative classes to model data pipelines while
delegating execution to best-in-class execution engines such as Pandas,
Polars, Airflow, and future plugins.

## Documentation Guide

### Start Here

-   **PIPELINEMODEL_MANIFESTO.md** --- The philosophy and vision of the
    project.
-   **01_GETTING_STARTED/** --- Installation, quickstart, and your first
    pipeline.

### Learn the Foundations

-   **02_FOUNDATIONS/** --- Core concepts, design principles, and
    architecture.

### Build Pipelines

-   **03_DATA_CONTRACTS/** --- Author ContractModel-compatible data
    contracts (ODCS).
-   **04_TRANSFORMATIONS/** --- Define typed transformation contracts
    (DTCS).
-   **05_PIPELINES/** --- Wire contracts together into typed pipelines
    (DPCS).

### Execute Pipelines

-   **06_EXECUTION/** --- Execution model, plugins, bindings, and
    runtime profiles.

### Extend PipelineModel

-   **07_PLUGIN_SDK/** --- Build custom execution, orchestration, and
    storage plugins.

### Visualize and Document

-   **08_VISUALIZATION/** --- Lineage, diagrams, documentation
    generation, and graph exports.

### Explore Examples

-   **09_EXAMPLES/** --- End-to-end examples, migration guides, and
    reference projects.

### API and Reference

-   **10_REFERENCE/** --- CLI, configuration, diagnostics, exceptions,
    and API reference.

### Contribute

-   **11_DEVELOPMENT/** --- Roadmap, architecture decisions, testing,
    and contribution guidelines.

## Guiding Philosophy

PipelineModel follows a few simple principles:

-   Python type annotations are the source of truth.
-   Contracts are generated from code whenever possible.
-   Pipelines model intent, not execution.
-   Execution is delegated to interchangeable plugins.
-   Validation happens before execution.
-   One pipeline should be portable across multiple execution
    environments.

## Relationship to Other Projects

PipelineModel is part of a larger ecosystem:

-   **ContractModel** --- Operationalizes data contracts.
-   **ODCS** --- Open Data Contract Standard.
-   **DTCS** --- Data Transformation Contract Standard.
-   **DPCS** --- Data Pipeline Contract Standard.

PipelineModel unifies these standards into a single typed authoring
experience while remaining execution-engine independent.

## Recommended Reading Order

1.  PipelineModel Manifesto
2.  Getting Started
3.  Foundations
4.  Data Contracts
5.  Transformations
6.  Pipelines
7.  Execution
8.  Plugin SDK
9.  Examples
10. Reference

Happy building!
