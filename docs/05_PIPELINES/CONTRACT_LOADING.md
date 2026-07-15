# Contract Loading

Contract loading allows PipelineModel to construct in-memory models from
portable contract artifacts.

While PipelineModel recommends a **code-first** workflow using strongly typed
Python classes, it also supports **contract-first** workflows by loading ODCS,
DTCS, and DPCS artifacts into the same internal object model.

This enables interoperability with external tools, registries, and existing
contract repositories.

## Goals

Contract loading should:

- Support code-first and contract-first workflows.
- Produce the same internal models regardless of source.
- Validate contracts during loading.
- Resolve references automatically.
- Preserve identities and semantics.
- Remain independent of serialization formats.

## Philosophy

Whether authored in Python or YAML, a contract should become the same logical
model.

```text
Python Classes          YAML / JSON Contracts
       │                        │
       └────────────┬───────────┘
                    ▼
             Contract Loader
                    ▼
        Canonical Object Model
                    ▼
          Validation & Planning
```

The source format should not affect pipeline behavior.

## Supported Contract Types

PipelineModel can load:

- ODCS Data Contracts
- DTCS Transformation Contracts
- DPCS Pipeline Contracts

Each contract is normalized into the same internal representation used by the
code-first APIs.

## Loading APIs

Conceptually:

```python
from pipelinemodel import DataContractModel, Pipeline, Transformation

customer = DataContractModel.from_odcs("customer.odcs.yaml")

normalize = Transformation.from_dtcs(
    "normalize.dtcs.yaml",
)

pipeline = Pipeline.from_dpcs(
    "customer_pipeline.dpcs.yaml",
)
```

Future APIs may support loading from streams, registries, packages, or remote
URLs.

## Canonical Object Model

All loaded contracts are normalized into a common in-memory representation.

The canonical model preserves:

- Identity
- Metadata
- Interfaces
- References
- Graph topology
- Version information
- Compatibility metadata
- Extensions

Planning and execution operate on the canonical model rather than raw files.

## Reference Resolution

Contracts frequently reference one another.

Examples include:

- DPCS → DTCS
- DTCS → ODCS
- DPCS → nested DPCS

The loader resolves these references before planning.

Resolution sources may include:

- Local directories
- Python packages
- Git repositories
- Contract registries
- Organization-specific providers

## Validation During Loading

Loading performs structural validation before contracts become usable.

Checks may include:

- Required fields
- Schema correctness
- Version compatibility
- Identifier validity
- Reference integrity
- Extension validity

Invalid contracts should fail before planning begins.

## Serialization Independence

PipelineModel separates semantics from serialization.

Equivalent contracts expressed as:

- YAML
- JSON
- TOML (future)

should produce identical canonical models.

## Caching

Implementations may cache loaded contracts to improve performance.

Cached contracts should be invalidated when:

- Source files change
- Contract versions change
- Registry revisions change
- Compatibility requirements change

## Registry Integration

Contract loading integrates naturally with contract registries.

Conceptually:

```python
pipeline = Pipeline.from_registry(
    "customer-pipeline",
    version="1.2.0",
)
```

Registry implementations remain pluggable.

## Relationship to Planning

Loading precedes planning.

```text
Contract Files
      │
      ▼
Loading
      │
      ▼
Canonical Object Model
      │
      ▼
Validation
      │
      ▼
Pipeline Plan
```

Planning never depends on the original file format.

## Relationship to Generation

Generation and loading are complementary.

```text
Python
   │
   ▼
Generate Contracts
   │
   ▼
Portable Artifacts
   │
   ▼
Load Contracts
   │
   ▼
Canonical Object Model
```

A generated contract should load into an equivalent internal model.

## Best Practices

- Treat generated contracts as portable artifacts.
- Validate during loading.
- Resolve references before planning.
- Prefer stable identifiers over file paths.
- Cache immutable contracts where appropriate.

## Anti-Patterns

Avoid:

- Depending on serialization-specific behavior.
- Skipping validation during loading.
- Using file paths as contract identities.
- Mutating loaded contracts in place.
- Loading contracts that cannot resolve required references.

## Key Principle

> Contract loading converts portable ODCS, DTCS, and DPCS artifacts into a
canonical PipelineModel object model that is independent of serialization,
storage location, and authoring workflow.

## Next Step

Continue with **PIPELINE_REGISTRY.md** to learn how contracts are published,
discovered, and shared across teams.
