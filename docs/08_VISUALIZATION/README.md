# Visualization

Visualization transforms PipelineModel artifacts into diagrams, interactive views,
and documentation that help developers understand pipelines without reading
implementation code.

Visualization is built on the same validated Pipeline Plan used for execution,
ensuring every diagram reflects the true logical pipeline.

## Purpose

This section covers:

- Pipeline graphs
- Data lineage
- Contract relationships
- Dependency graphs
- Execution plans
- Interactive explorers
- Documentation generation
- IDE integration

## Philosophy

Never visualize source code directly.

Always visualize the validated model.

```text
Python Pipeline
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
Visualization
      ├── Mermaid
      ├── Graphviz
      ├── HTML
      ├── SVG
      └── Interactive UI
```

## Visualization Types

PipelineModel is designed to support:

- Pipeline DAGs
- Source-to-sink flow diagrams
- Contract relationship graphs
- Transformation dependency graphs
- Lineage diagrams
- Execution timelines
- Plugin architecture diagrams
- Planning diagnostics

## Benefits

Visualization should:

- Improve documentation
- Aid debugging
- Support architecture reviews
- Explain pipeline behavior
- Verify graph structure
- Communicate lineage

## Relationship to Planning

Visualizations are generated from the Pipeline Plan rather than execution
artifacts. This keeps diagrams backend-independent and deterministic.

## Documentation Roadmap

Suggested reading order:

1. PIPELINE_GRAPHS.md
2. LINEAGE.md
3. MERMAID.md
4. GRAPHVIZ.md
5. HTML.md
6. SVG.md
7. INTERACTIVE.md
8. DOCUMENTATION.md

## Best Practices

- Visualize validated plans only.
- Keep diagrams deterministic.
- Preserve stable node identities.
- Distinguish logical semantics from runtime details.
- Generate documentation automatically.

## Key Principle

> Visualization is another consumer of the Pipeline Plan. Like execution,
> documentation and diagrams derive from the same canonical intermediate
> representation, guaranteeing they remain synchronized with the modeled
> pipeline.

## Next Step

Continue with **PIPELINE_GRAPHS.md** to explore graph generation from Pipeline
Plans.
