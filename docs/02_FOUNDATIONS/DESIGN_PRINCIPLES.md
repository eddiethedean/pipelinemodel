# Design Principles

These principles guide every architectural and API decision in
PipelineModel. They are intended to keep the framework focused,
predictable, and consistent as it evolves.

## 1. Types Are the Source of Truth

Python type annotations define pipeline interfaces.

From those types, PipelineModel should infer contracts, validation
rules, documentation, and editor tooling whenever possible.

Developers should not have to describe the same interface multiple
times.

------------------------------------------------------------------------

## 2. Model Before You Execute

PipelineModel models **what** a pipeline is.

Execution engines determine **how** that pipeline runs.

Modeling concerns belong in PipelineModel.

Execution concerns belong in plugins.

------------------------------------------------------------------------

## 3. Separate Logic from Runtime

Business logic should not depend on a specific dataframe library,
scheduler, or cloud provider.

The same logical pipeline should be able to execute through different
runtime profiles without changing its contract definitions.

------------------------------------------------------------------------

## 4. Prefer Code-First Authoring

Python classes are the preferred authoring experience.

Portable contract documents are generated from those classes whenever
practical.

PipelineModel should also support loading existing contracts, but
generated artifacts should remain faithful to the source model.

------------------------------------------------------------------------

## 5. Embrace Open Standards

PipelineModel builds on open specifications rather than proprietary
formats.

-   ODCS for data contracts
-   DTCS for transformation contracts
-   DPCS for pipeline contracts

Where an established standard exists, PipelineModel should integrate
with it rather than reinvent it.

------------------------------------------------------------------------

## 6. Minimize Boilerplate

Never ask users to repeat information that can be inferred safely.

Examples include:

-   deriving contracts from type annotations
-   generating diagrams from pipeline topology
-   validating implementations against declared interfaces
-   producing documentation automatically

------------------------------------------------------------------------

## 7. Validate Early

Errors should be discovered during authoring and planning whenever
possible.

Validation should occur before expensive execution begins.

Clear diagnostics are preferred over runtime surprises.

------------------------------------------------------------------------

## 8. Keep the Core Small

PipelineModel should provide a stable modeling core.

Execution engines, storage systems, orchestration platforms, and
integrations should be implemented as plugins.

A small core is easier to learn, test, and evolve.

------------------------------------------------------------------------

## 9. Async Without Complexity

PipelineModel is asynchronous internally.

Users may write either synchronous (`def`) or asynchronous (`async def`)
implementations.

The framework is responsible for choosing the correct invocation
strategy.

------------------------------------------------------------------------

## 10. Explicit Interfaces

Transformation interfaces should be obvious from their declarations.

``` python
class NormalizeCustomers(Transformation):
    customers: Input[RawCustomer]
    minimum_age: Parameter[int] = 18
    result: Output[Customer]
```

A reader should understand the transformation without reading its
implementation.

------------------------------------------------------------------------

## 11. Portability First

Pipelines should be portable across:

-   execution engines
-   environments
-   organizations
-   deployment targets

Contracts and models should outlive any individual runtime technology.

------------------------------------------------------------------------

## 12. Optimize for Developer Experience

PipelineModel should feel natural to Python developers.

Good defaults, strong typing, meaningful errors, autocomplete, and
generated documentation are not optional---they are part of the
framework's value.

------------------------------------------------------------------------

## Decision Filter

When evaluating a new feature, ask:

1.  Does it improve the modeling experience?
2.  Can it be expressed through types or declarative models?
3.  Does it reduce duplication?
4.  Does it preserve runtime independence?
5.  Does it belong in the core rather than a plugin?

If the answer to the last question is "no," the feature should likely be
implemented as a plugin instead.

## Relationship to Other Documents

-   **PIPELINEMODEL_MANIFESTO.md** defines the project's philosophy.
-   **VISION.md** defines where the project is headed.
-   **WHY_PIPELINEMODEL.md** explains why the project exists.
-   **FASTAPI_PHILOSOPHY.md** explains the design inspiration.

These design principles translate those ideas into practical
architectural rules that guide implementation.
