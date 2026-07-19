# Roadmap Summary

ETLantic is an alpha project moving toward a stable, secure modeling and plugin
platform. Milestones describe capability order, not release-date commitments.

## 0.15 shipped

ETLantic 0.15.0 closed the Safe SQL Lowering exit gate and the LocalScheduler
companion:

- `etlantic-sql` claims kernel + `portable-relational/1` through typed
  `etlantic.sql/1` IR (PostgreSQL reference dialect; bound parameters only);
- Extract / Load / `asset=` is the preferred authoring vocabulary
  (`Source` / `Sink` / `binding=` warn; remove in 0.16);
- `Pipeline.run` / `arun` enter through built-in `LocalScheduler`;
- public portable conformance covers Polars, PySpark, Pandas, and SQL.

See [What's New in 0.15](../01_GETTING_STARTED/WHATS_NEW_0_15.md) and
[Capabilities](../01_GETTING_STARTED/CAPABILITIES.md) for the shipped boundary.

### 0.15 continuation (not required to close 0.15)

Richer portable profiles (window, string-advanced, conversion, complex
types/values, statistics, reshape, relational-extended, temporal-IANA,
nondeterministic) graduate **one family at a time** only after two independent
compilers pass shared fixtures. That work is sequenced after the SQL vertical
slice; it is not a separate 0.16 milestone.

## Prior: 0.14

ETLantic 0.14.0 completed the first three-engine portable relational baseline
(Pandas joined Polars and PySpark) and published the public portable
conformance SDK. See [What's New in 0.14](../01_GETTING_STARTED/WHATS_NEW_0_14.md).

## Next: 0.16 (Optional Prefect orchestration)

- publish optional `etlantic-prefect` as the reference Python-native
  orchestrator integration;
- consume resolved physical execution units without re-planning;
- preserve ETLantic-owned validation, retry safety, identities, artifacts,
  redaction, and run reports;
- support a basic local Prefect path without requiring Prefect Cloud;
- keep local execution as the default and require explicit production profile
  selection/allowlisting;
- retain `etlantic-airflow` as the reference external compiler;
- remove the deprecated 0.15 `Source` / `Sink` / `binding=` compatibility API.

See the
[Local Scheduler and Prefect Integration Plan](SCHEDULER_AND_PREFECT_PLAN.md)
(Prefect packaging remains 0.16; feasibility notes live in-repo only).

## Toward 1.0

The 1.0 goal is a stable foundation with:

- stable authoring, Plugin SDK, plan, event, result, and run-report contracts;
- documented compatibility, deprecation, and schema-migration policies;
- completed security gates for plugin provenance, secret handling, artifact and
  cache isolation, network constraints, audit evidence, and bounded work;
- conformance and acceptance coverage across reference engines and
  orchestrators;
- complete executable tutorials, references, and migration guides.

> **Do not productionize ETLantic before the 1.0 security release gate
> closes.** Version 0.15.0 is alpha; available allowlists and version pins do
> not make the product production-ready. See the
> [Evaluator Brief](../01_GETTING_STARTED/EVALUATOR.md).

Read the
[full roadmap](https://github.com/eddiethedean/etlantic/blob/main/ROADMAP.md)
for milestone details, acceptance scenarios, and release gates.
