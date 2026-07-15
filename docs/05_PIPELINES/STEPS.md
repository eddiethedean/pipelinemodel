# Steps

A `Step` is a concrete instance of a `Transformation` inside a `Pipeline`.

A `Transformation` defines a reusable contract. A `Step` binds that contract to
specific inputs, parameter values, and downstream connections, making it part
of a pipeline graph.

## Purpose

Steps answer one question:

> Where and how is this transformation used in this pipeline?

A transformation may be reused multiple times, producing multiple independent
steps.

## Transformation vs. Step

```python
class NormalizeCustomers(Transformation):
    customers: Input[RawCustomer]
    minimum_age: Parameter[int] = 18
    result: Output[Customer]
```

Reusable transformation.

```python
normalized = NormalizeCustomers.step(
    customers=raw,
    minimum_age=21,
)
```

Concrete pipeline step.

## Why Steps Exist

Separating transformations from steps allows:

- Reusable transformation definitions
- Multiple instances of the same transformation
- Different parameter values
- Different pipeline graphs
- Stable DTCS contracts with many DPCS references

## Inputs

Steps bind upstream outputs to transformation inputs.

```python
NormalizeCustomers.step(
    customers=raw.result,
)
```

PipelineModel validates compatibility before planning.

## Parameters

Each step may override parameter defaults.

```python
NormalizeCustomers.step(
    customers=raw.result,
    minimum_age=25,
)
```

The transformation contract is unchanged; only this step's configuration differs.

## Outputs

Outputs become typed references for downstream steps.

```python
validated = ValidateCustomers.step(
    customers=normalized.result,
)
```

## Identity

Every step should have a stable identity within its pipeline.

Conceptually:

- Step name
- Transformation identity
- Pipeline identity
- Parameter values
- Input bindings

This identity supports lineage, diagnostics, and execution planning.

## Planning

During planning, each step becomes a node in the execution graph.

The planner resolves:

- Dependencies
- Execution order
- Parallel opportunities
- Runtime implementation
- Validation policy

## Relationship to DPCS

Each step is represented in the generated DPCS artifact with:

- Transformation reference
- Input bindings
- Output bindings
- Parameter values
- Metadata

The transformation itself remains defined by DTCS.

## Best Practices

- Keep transformations reusable.
- Instantiate them with `.step()`.
- Use descriptive step names.
- Override only necessary parameters.
- Let outputs feed downstream inputs.

## Anti-Patterns

Avoid:

- Embedding business logic in pipeline definitions.
- Duplicating transformation definitions for different parameter values.
- Referencing runtime-specific objects in step declarations.

## Key Principle

> A `Transformation` defines a reusable operation. A `Step` is one use of that
operation within a specific pipeline.

## Next Step

Continue with **SINKS.md** to learn how pipelines publish validated outputs.
