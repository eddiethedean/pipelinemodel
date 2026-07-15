# Pipelines

Pipelines connect typed transformations into complete, executable data workflows.

If **Data Contracts** define *what* data looks like and **Transformations**
define *how* data changes, then **Pipelines** define *how those transformations
are connected*.

PipelineModel models pipelines using the **Data Pipeline Contract Standard
(DPCS)** while remaining independent of any execution engine.

## What This Section Covers

This section explains how to:

- Define pipelines with Python classes
- Connect transformations using typed inputs and outputs
- Declare sources and sinks
- Configure execution profiles
- Validate pipeline graphs
- Generate DPCS artifacts
- Plan execution
- Produce lineage and documentation

## The Authoring Model

A pipeline is declared using ordinary Python.

```python
class CustomerPipeline(Pipeline):
    raw = CsvSource[RawCustomer](path="customers.csv")

    normalized = NormalizeCustomers.step(
        customers=raw,
        minimum_age=18,
    )

    warehouse = SqlSink[Customer](
        input=normalized.result,
    )
```

The declaration focuses on the logical flow of data rather than execution
details.

## Relationship to DPCS

Every pipeline has a portable representation.

```text
Python Pipeline
       │
       ▼
PipelineModel
       │
       ▼
DPCS Pipeline Contract
```

Python is the preferred authoring experience.

DPCS is the portable artifact.

## Planning vs. Execution

PipelineModel separates planning from execution.

Planning determines:

- Graph topology
- Contract compatibility
- Implementation selection
- Validation policy
- Execution profile
- Runtime bindings

Execution plugins perform the actual work.

## Sources and Sinks

Pipelines begin with typed sources and end with typed sinks.

```text
Source
   │
   ▼
Transformation
   │
   ▼
Transformation
   │
   ▼
Sink
```

Every connection is validated through data contracts.

## Validation

Before execution, PipelineModel validates:

- Graph structure
- Contract compatibility
- Required bindings
- Transformation implementations
- Execution profile
- Plugin capabilities

Planning should fail before execution whenever possible.

## Generated Artifacts

A pipeline can generate:

- DPCS contracts
- Documentation
- Mermaid diagrams
- Graphviz diagrams
- Lineage graphs
- Execution plans

Generated artifacts are deterministic and suitable for version control.

## Documentation Roadmap

Read this section in the following order:

1. PIPELINE.md
2. SOURCES.md
3. SINKS.md
4. PIPELINE_GRAPH.md
5. EXECUTION_PROFILES.md
6. PLANNING.md
7. DPCS.md
8. GENERATION.md

## Key Principles

- Pipelines connect transformations.
- Data contracts validate every connection.
- Planning precedes execution.
- Execution belongs to plugins.
- DPCS is the canonical portable representation.
- Python remains the preferred authoring experience.

## Next Step

Continue with **PIPELINE.md** to learn how to define typed pipeline classes and
compose transformations into complete workflows.
