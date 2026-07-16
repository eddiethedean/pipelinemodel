# Pandas

The Pandas plugin enables Pipelantic to execute transformations using the
Pandas dataframe library.

Pandas is one of the most widely adopted data analysis libraries in Python and
provides excellent compatibility with the broader data ecosystem. Pipelantic
supports Pandas as an execution backend while encouraging users to keep their
contracts and pipeline definitions independent of any dataframe library.

## Goals

The Pandas plugin should:

- Execute DTCS transformation implementations using Pandas.
- Preserve Pipelantic semantics.
- Integrate with execution profiles.
- Interoperate with existing Pandas-based code.
- Remain interchangeable with other dataframe plugins.

## Philosophy

Pipeline authors should never write pipelines that depend on Pandas.

Instead, they define portable contracts:

```python
class NormalizeCustomers(Transformation):
    customers: Input[RawCustomer]
    result: Output[Customer]
```

The execution profile selects the Pandas implementation.

```python
@NormalizeCustomers.implementation("pandas")
def normalize(customers, minimum_age):
    ...
```

## Why Pandas?

Pandas provides:

- Mature ecosystem
- Extensive third-party integrations
- Familiar APIs
- Broad community support
- Excellent compatibility with existing Python projects

These strengths make it an important compatibility backend.

## Recommended Usage

Pipelantic recommends:

- Use Polars for new high-performance workloads.
- Use Pandas when integrating with existing libraries or legacy code.
- Keep contracts independent of dataframe implementations.

## Execution Profile

Example:

```python
production = Profile(
    dataframe_engine="pandas",
)
```

Planning selects Pandas implementations for compatible transformations.

## Supported Features

The Pandas plugin should support:

- Typed transformation execution
- Contract validation
- Sync execution
- Async execution (through Pipelantic)
- Callback integration
- Structured diagnostics

## Limitations

Compared with modern dataframe engines, Pandas may offer:

- Less efficient parallel execution
- Higher memory usage
- Limited lazy evaluation

These characteristics affect performance, not pipeline semantics.

## Relationship to Other Plugins

The same transformation may provide multiple implementations.

```python
@NormalizeCustomers.implementation("polars")
def normalize_polars(...):
    ...

@NormalizeCustomers.implementation("pandas")
def normalize_pandas(...):
    ...
```

Pipelantic selects the implementation using the active profile.

## Best Practices

- Keep transformation contracts dataframe-independent.
- Reuse existing Pandas code where appropriate.
- Validate outputs before publication.
- Avoid exposing DataFrame objects outside execution plugins.

## Anti-Patterns

Avoid:

- Using Pandas types in public pipeline interfaces.
- Writing Pandas-specific pipeline definitions.
- Depending on Pandas for contract semantics.
- Mixing Pandas APIs into data contracts.

## Key Principle

> Pandas is an execution backend, not a modeling dependency. Pipelantic
preserves identical pipeline semantics regardless of whether a transformation
executes with Pandas, Polars, or another supported dataframe engine.

## Next Step

Continue with **POLARS.md** to learn about the recommended high-performance
reference dataframe plugin for Pipelantic.
