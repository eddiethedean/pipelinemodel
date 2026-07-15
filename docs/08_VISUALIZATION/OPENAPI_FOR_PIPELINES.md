# OpenAPI for Pipelines

PipelineModel can generate an **OpenAPI-like specification for data pipelines**.

Just as OpenAPI standardizes HTTP APIs, PipelineModel standardizes the public
interface of a pipeline. This specification describes *what a pipeline accepts,
what it produces, and how it behaves* without exposing implementation details.

The generated specification is intended for documentation, discovery,
governance, validation, IDE tooling, registries, and interoperability.

## Purpose

An OpenAPI-style pipeline specification enables:

- Pipeline discovery
- Automatic documentation
- Client generation
- Contract validation
- Dependency analysis
- Registry publication
- Governance
- Impact analysis

## Philosophy

Treat pipelines as products with well-defined interfaces.

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
Pipeline Plan (IR)
    │
    ▼
Pipeline OpenAPI Generator
    │
    ▼
OpenAPI-like Specification
```

The specification is generated from the validated model and is never the source
of truth.

## Why an OpenAPI Analogy?

OpenAPI answers questions such as:

- What endpoints exist?
- What parameters are accepted?
- What schemas are exchanged?

PipelineModel answers analogous questions:

- What sources exist?
- What parameters are accepted?
- What contracts are consumed?
- What contracts are produced?
- What quality gates exist?
- What execution requirements exist?

## Specification Structure

Conceptually:

```yaml
pipeline:
  id: customer-curation
  version: 1.2.0

inputs:
  - RawCustomer

outputs:
  - Customer

transformations:
  - NormalizeCustomers
  - ValidateCustomers

contracts:
  odcs:
    - customer
  dtcs:
    - normalize-customers
  dpcs:
    - customer-curation
```

The actual schema is defined by PipelineModel and evolves independently.

## Public Interface

A generated specification may include:

- Pipeline identity
- Version
- Description
- Owners
- Tags
- Inputs
- Outputs
- Parameters
- Source bindings
- Sink bindings
- Referenced contracts
- Quality gates
- Failure policies
- Capability requirements
- Compatibility metadata

## Relationship to Standards

The specification references, rather than replaces:

- ODCS (data contracts)
- DTCS (transformation contracts)
- DPCS (pipeline contracts)

It acts as an integration document across those standards.

## Tooling

The specification may power:

- Documentation sites
- Interactive explorers
- IDE support
- Search indexes
- Pipeline registries
- Dependency visualizers
- Governance dashboards

## Generation

Conceptually:

```python
spec = pipeline.to_openapi()
```

or

```python
plan.write_openapi("customer-pipeline.yaml")
```

Generation should consume the validated Pipeline Plan.

## Versioning

Every generated specification should declare:

- PipelineModel version
- Specification version
- Pipeline version
- Referenced contract versions
- Compatibility metadata

## Determinism

Equivalent Pipeline Plans should generate semantically equivalent specifications.

Stable ordering should be used for:

- Objects
- Parameters
- Contracts
- References
- Tags

## Security

Generated specifications should never include:

- Secrets
- Credentials
- Runtime tokens
- Physical infrastructure details

Logical bindings may be included when appropriate.

## Best Practices

- Generate specifications automatically.
- Treat them as derived artifacts.
- Reference canonical contracts.
- Publish explicit versions.
- Keep them deterministic.
- Validate in CI.

## Anti-Patterns

Avoid:

- Editing generated specifications manually.
- Treating specifications as executable pipelines.
- Embedding runtime secrets.
- Duplicating contract definitions instead of referencing them.

## Comparison

| HTTP APIs | PipelineModel |
|-----------|---------------|
| OpenAPI | Pipeline OpenAPI |
| Endpoint | Pipeline |
| Request schema | Input contract |
| Response schema | Output contract |
| Operation | Transformation |
| Tags | Domains / Labels |
| Components | Shared contracts |

## Future Directions

Future versions may support:

- Registry discovery
- JSON Schema generation
- Client SDK generation
- Governance integrations
- Catalog synchronization
- Interactive documentation

## Key Principle

> An OpenAPI-style pipeline specification provides a portable, machine-readable
description of a pipeline's public interface. Like OpenAPI, it documents the
contract—not the implementation—and is generated directly from PipelineModel's
canonical models.

## Next Step

Continue with **INTERACTIVE.md** to explore interactive visualization,
inspection, and navigation of generated pipeline specifications.
