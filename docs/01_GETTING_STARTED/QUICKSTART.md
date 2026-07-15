# Quickstart

Welcome to your first PipelineModel project.

In this guide you'll build a complete, typed pipeline in just a few
minutes. You'll define a data contract, create a transformation
contract, wire everything into a pipeline, validate it, and generate
portable contracts.

> **Goal:** Learn the PipelineModel mental model, not every feature.

## Step 1 --- Define a Data Contract

``` python
from contractmodel import DataContractModel

class Customer(DataContractModel):
    id: int
    first_name: str
    last_name: str
```

This class is both a Pydantic model and the source of an ODCS-compatible
data contract.

## Step 2 --- Define a Transformation

``` python
from pipelinemodel import Transformation, Input, Output

class NormalizeCustomers(Transformation):
    customers: Input[Customer]
    result: Output[Customer]
```

The type annotations describe the transformation interface.
PipelineModel can derive a DTCS contract from this definition.

## Step 3 --- Build a Pipeline

``` python
from pipelinemodel import Pipeline, Source, Sink

class CustomerPipeline(Pipeline):
    raw = Source(contract=Customer)

    normalized = NormalizeCustomers.step(
        customers=raw,
    )

    curated = Sink(
        contract=Customer,
        input=normalized.result,
    )
```

Notice that the pipeline describes **logical data flow** rather than
execution.

## Step 4 --- Validate

``` python
report = CustomerPipeline.validate()

if report.has_errors:
    report.raise_for_errors()
```

Validation happens before execution so wiring and contract mismatches
are caught early.

## Step 5 --- Generate Contracts

``` python
CustomerPipeline.write_contracts("contracts/")
```

PipelineModel generates:

``` text
contracts/
├── data/
│   └── customer.odcs.yaml
├── transformations/
│   └── normalize-customers.dtcs.yaml
└── pipelines/
    └── customer-pipeline.dpcs.yaml
```

## Step 6 --- Execute

Choose the execution engine appropriate for your environment.

``` python
CustomerPipeline.run(
    profile="local",
)
```

or

``` python
await CustomerPipeline.arun(
    profile="production",
)
```

PipelineModel handles synchronous and asynchronous implementations
transparently while delegating actual execution to plugins.

## What You've Learned

You have:

-   Defined a typed data contract.
-   Defined a typed transformation.
-   Built a pipeline.
-   Validated the pipeline.
-   Generated portable contracts.
-   Executed through a runtime profile.

## Where to Go Next

Continue with **FIRST_PIPELINE.md**, where you'll build a realistic
end-to-end ETL pipeline and learn how data contracts, transformation
contracts, and pipeline contracts work together.
