# Roadmap Summary

ETLantic is an alpha project moving toward a stable, secure modeling and plugin
platform. Milestones describe capability order, not release-date commitments.

## Shipped: 0.15, 0.16, and 0.17

ETLantic **0.15.0** closed Safe SQL Lowering and the LocalScheduler companion.

ETLantic **0.16.0** shipped Gate A (authoring vocabulary cleanup) and Gate B
(optional `etlantic-prefect` `ExecutionScheduler`).

ETLantic **0.17.0** shipped portable coverage expansion:

- Gate A — transform-compiler CLI inventory, exact capability matrix, drift
  checks, allowlist-safe discovery
- Gate B — Wave 1 on Polars + PySpark (`portable-window/1`,
  `portable-string-advanced/1`, `portable-conversion/1`,
  `portable-statistics/1`)
- Gate C — Wave 2 on Polars + PySpark (`portable-complex-types/1`,
  `portable-complex-values/1`, `portable-reshape/1`)

Pandas and SQL remain kernel + `portable-relational/1` in 0.17. See
[What's New in 0.17](../01_GETTING_STARTED/WHATS_NEW_0_17.md) and
[Migration 0.16 → 0.17](MIGRATION_0_16_TO_0_17.md).

**0.17 continuation** (not required to close 0.17):
`portable-relational-extended/1`, `portable-temporal-iana/1`,
`portable-nondeterministic/1`, `portable-window/2`.

## Prior: 0.14

ETLantic 0.14.0 completed the first three-engine portable relational baseline
and published the public portable conformance SDK. See
[What's New in 0.14](../01_GETTING_STARTED/WHATS_NEW_0_14.md).

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
> closes.** Version 0.17.0 is alpha; available allowlists and version pins do
> not make the product production-ready. See the
> [Evaluator Brief](../01_GETTING_STARTED/EVALUATOR.md).

Read the
[full roadmap](https://github.com/eddiethedean/etlantic/blob/main/ROADMAP.md)
for milestone details, acceptance scenarios, and release gates.
