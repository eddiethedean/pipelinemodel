# What's New in 0.22

ETLantic **0.22.0** is the **Plugin SDK Release Candidate**: capability-driven
engine identity, a versioned capability vocabulary, hardened public conformance,
a curated `import etlantic as etl` facade, a compatibility-report CLI, and an
out-of-monorepo reference plugin.

Protocol `/1` families are **freeze-eligible**, not frozen — see
[Protocol Evolution](../07_PLUGIN_SDK/PROTOCOL_EVOLUTION.md) and
[Exit Gate 0.22](../11_DEVELOPMENT/EXIT_GATE_0_22.md).

## Recommended import style

```python
import etlantic as etl

class Customer(etl.Data):
    customer_id: int
    name: str
```

Curated root symbols plus lazy namespaces (`etl.sql`, `etl.testing`, …).
Specialist root exports demoted in 0.22 remain as warn-once compatibility
aliases. See [Surface Inventory](../10_REFERENCE/SURFACE_INVENTORY.md).

## Capability-driven engines

Planning, discovery, and runtime no longer privilege first-party engine name
sets. Third-party engines validate → plan → run/compile → report → viz via
authorized descriptors and `PluginCapabilities`.

## Capability vocabulary `/1`

`etlantic.capabilities/1` is versioned independently with published
implication / conflict / deprecation rules. Overstated claims fail conformance
with actionable findings.

## Conformance hardening

- Dataframe suite is capability-driven (no `engine == "pandas"` special cases)
- SQL suite: redaction + malformed-output guards
- **New** `run_spark_conformance_suite` (session-free)
- Shared `assert_capability_claims_consistent` /
  `assert_capability_matches_behavior`
- First-party plugins exercise public `etlantic.testing` entry points only

## Compatibility CLI

```bash
etlantic plugin compatibility etlantic-polars --format json
etlantic plugin compatibility --format human
```

## External proof

Public reference plugin:
[eddiethedean/etlantic-plugin-echo](https://github.com/eddiethedean/etlantic-plugin-echo)
(engine `echo`). Monorepo CI clones and runs its public suites against workspace
core (`.github/workflows/external-plugin-echo.yml`).

## Typed protocol metadata

`ExecutionContextMeta` / `CompileArtifactMeta` (and coerce helpers) type
stability-critical context/artifact metadata on dataframe, SQL, and Spark
boundaries. Extension bags stay under `etlantic.` / `plugin:` namespaces.

## Migration

See [Migration 0.21 → 0.22](../11_DEVELOPMENT/MIGRATION_0_21_TO_0_22.md).
