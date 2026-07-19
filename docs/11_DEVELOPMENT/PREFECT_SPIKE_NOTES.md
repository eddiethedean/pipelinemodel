# Prefect Feasibility Spike (0.15)

Status: notes only — **not** a release dependency  
Package target: optional `etlantic-prefect` in **0.16**

## Goal

Prove that a Prefect adapter can consume a resolved `PipelinePlan` through the
same [`ExecutionScheduler`](../../src/etlantic/runtime/scheduler.py) boundary as
`LocalScheduler`, without re-planning or becoming a core dependency.

## Findings (spike)

1. **Boundary:** `LocalScheduler.analyze` / `execute` is sufficient as the
   direct-execution contract. Prefect should implement the same protocol in
   0.16 rather than inventing a second discovery system.
2. **Units:** 0.15 still schedules logical graph nodes via the runtime host.
   Prefect task mapping should target `plan.physical_units` once fusion-driven
   unit scheduling is complete; until then, map one task per selected logical
   node with the same dependency closure.
3. **Ownership:** Prefect must not own validation, materialization,
   retry-safety, redaction, or `PipelineRunReport` construction.
4. **Default path:** Prefect remains absent from core imports and from the
   default `development` / `test` profiles.

## Non-goals for the spike

- Publishing `etlantic-prefect`
- Changing production profile defaults
- Replacing `etlantic-airflow` compilation

## Follow-ups for 0.16

- Map physical units → Prefect flows/tasks
- Correlate ETLantic run/unit ids with Prefect flow/task-run ids
- Shared public conformance fixtures with `LocalScheduler`
- Explicit `Profile(orchestrator="prefect")` + plugin allowlisting
