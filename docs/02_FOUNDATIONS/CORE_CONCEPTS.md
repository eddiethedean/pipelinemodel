# Core Concepts

PipelineModel is built around a small set of concepts. Understanding
these concepts is more important than memorizing APIs because every
feature in the framework is an extension of them.

## The Three-Layer Model

PipelineModel models a pipeline using three kinds of contracts:

``` text
Data Contracts
        │
        ▼
Transformation Contracts
        │
        ▼
Pipeline Contracts
```

Each layer has a distinct responsibility.

-   **Data Contracts** describe the structure and meaning of data.
-   **Transformation Contracts** describe how data flows between
    contracts.
-   **Pipeline Contracts** describe how transformations are connected
    into a complete pipeline.

## Data Contracts

Data contracts define datasets using ContractModel-compatible Pydantic
models.

``` python
class Customer(DataContractModel):
    id: int
    name: str
```

From this model PipelineModel can generate an ODCS-compliant contract.

Data contracts answer:

-   What data exists?
-   What fields does it contain?
-   What constraints apply?

They do **not** describe how the data is produced.

## Transformation Contracts

Transformation contracts define the interface of a transformation.

``` python
class NormalizeCustomers(Transformation):
    customers: Input[RawCustomer]
    result: Output[Customer]
```

A transformation contract describes:

-   inputs
-   outputs
-   parameters
-   metadata

It does **not** describe the execution engine.

A single transformation may have multiple implementations.

## Pipeline Contracts

Pipelines connect transformations together.

``` python
class CustomerPipeline(Pipeline):
    raw = Source(contract=RawCustomer)

    normalized = NormalizeCustomers.step(
        customers=raw,
    )

    curated = Sink(
        contract=Customer,
        input=normalized.result,
    )
```

The pipeline defines logical data flow, independent of execution.

## Implementations

Execution implementations perform the actual work.

``` python
@NormalizeCustomers.implementation("polars")
def normalize(df):
    ...
```

Another implementation might target Pandas, Spark, DuckDB, or a remote
service.

The contract remains unchanged.

## Plugins

PipelineModel delegates execution to plugins.

Examples include:

-   dataframe plugins
-   orchestration plugins
-   storage plugins
-   compiler plugins
-   resource providers

Plugins determine **how** work is performed.

PipelineModel determines **what** should happen.

## Profiles

Profiles bind a logical pipeline to a runtime environment.

``` python
CustomerPipeline.run(profile="local")
```

A profile may choose:

-   execution engine
-   orchestrator
-   storage provider
-   concurrency settings
-   environment-specific resources

The pipeline model itself remains unchanged.

## Validation

Validation occurs before execution.

PipelineModel verifies:

-   compatible contracts
-   pipeline wiring
-   parameter values
-   implementation compatibility
-   plugin bindings

This catches problems early and produces clear diagnostics.

## Planning

Before execution, PipelineModel creates an execution plan.

The plan resolves:

-   dependency order
-   runtime bindings
-   execution plugins
-   validation results

The plan can then be executed or compiled for an external orchestrator.

## Contracts as Artifacts

Python classes are the preferred authoring experience.

PipelineModel generates portable artifacts:

-   ODCS
-   DTCS
-   DPCS

These artifacts can be shared, versioned, reviewed, and consumed
independently of Python source code.

## The Modeling Lifecycle

Most projects follow the same lifecycle:

``` text
Define Data Contracts
          │
          ▼
Define Transformation Contracts
          │
          ▼
Build Pipeline
          │
          ▼
Validate
          │
          ▼
Generate Contracts
          │
          ▼
Plan Execution
          │
          ▼
Execute Through Plugins
```

## The Big Picture

PipelineModel deliberately separates concerns.

  Responsibility             Owner
  -------------------------- ---------------------------------
  Data semantics             Data Contracts (ODCS)
  Transformation semantics   Transformation Contracts (DTCS)
  Pipeline topology          Pipeline Contracts (DPCS)
  Authoring                  PipelineModel
  Data validation            ContractModel
  Execution                  Plugins
  Scheduling                 Orchestration plugins

This separation keeps the framework focused while allowing execution
technologies to evolve independently.

## Next Step

Continue with **ARCHITECTURE.md** to see how these concepts are
organized internally and how they interact within PipelineModel.
