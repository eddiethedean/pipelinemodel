# Local Scheduler and Prefect Integration Plan

Status: Accepted 0.15+ implementation plan  
Applies to: ETLantic core, `etlantic.orchestration`, and optional orchestrator packages  
Reference external compiler: `etlantic-airflow`  
Planned Python-native plugin: `etlantic-prefect`

## Decision

ETLantic will keep a small built-in local scheduler as the default development,
test, notebook, and embedded execution path. It will not embed Prefect,
Airflow, Dagster, or another orchestration framework in core.

ETLantic will:

1. Extract the domain-independent scheduling loop behind a stable scheduler
   boundary.
2. Keep ETLantic ownership of plan validation, asset resolution, plugin and
   implementation selection, physical regions, validation boundaries,
   materialization, output normalization, lifecycle events, redaction, and
   `PipelineRunReport` production.
3. Develop `etlantic-prefect` as the reference optional Python-native
   orchestration plugin.
4. Keep `etlantic-airflow` as the reference external artifact compiler.
5. Require every scheduler/orchestrator integration to consume a resolved
   `PipelinePlan` without re-planning it or changing observable semantics.

Prefect is not the automatic default for `development`, `test`, or
`production`. Production profiles select and allowlist an orchestrator
explicitly.

## Why retain a built-in scheduler

The local runner is more than a generic topological executor. It coordinates
ETLantic-specific semantics that no general orchestrator should own:

- Extract and Load execution boundaries
- native and portable transformation realization
- dataframe, SQL, and Spark execution regions
- typed input/output validation
- valid, invalid, and side output roles
- materialization and ownership boundaries
- retries, idempotency, callbacks, and partial-run selection
- logical identity, diagnostics, redaction, and run reports

Replacing the local runner with Prefect would still require an ETLantic adapter
containing most of this logic while adding Prefect's task, state, configuration,
and deployment model. The built-in path therefore remains the smallest
zero-service execution kernel.

## Architectural boundaries

```text
Pipeline + Profile
        ↓
validated, resolved PipelinePlan
        ↓
ETLantic physical execution units
        ↓
ExecutionScheduler
   ├── LocalScheduler          built in and default
   └── PrefectScheduler        optional etlantic-prefect

PipelinePlan
        ↓
Orchestrator compiler
   └── Airflow DAG             optional etlantic-airflow
```

The scheduler boundary coordinates ready physical units. It does not compile
DTCS expressions, execute dataframe operations itself, resolve secrets during
planning, or invent retry/materialization semantics.

## Proposed scheduler boundary

The exact API is finalized through implementation pressure, but its conceptual
shape is:

```python
@runtime_checkable
class ExecutionScheduler(Protocol):
    @property
    def info(self) -> SchedulerInfo: ...

    def analyze(
        self,
        plan: PipelinePlan,
        *,
        context: SchedulingContext,
    ) -> SchedulerSupportReport: ...

    async def execute(
        self,
        plan: PipelinePlan,
        *,
        runtime: PipelineRuntime,
        context: SchedulingContext,
    ) -> PipelineRunReport: ...
```

`analyze()` is deterministic, side-effect free, and fail closed. `execute()`
receives the already-resolved plan and application-owned runtime services.

Required scheduler capabilities include only coordination concerns such as:

- dependency scheduling
- bounded concurrency
- sync/async callable dispatch
- cancellation and timeouts
- safe retries
- partial-run selection
- lifecycle event correlation
- artifact handoff

Engine, storage, transformation, and contract capabilities remain owned by
their existing plugins and plan descriptors.

## Relationship to `etlantic.orchestration/1`

The shipped orchestration protocol primarily models deterministic compilation,
submission, polling, cancellation, and correlation for external platforms.
The scheduler boundary is the direct-execution companion to that protocol.

0.15 must decide whether to:

- add direct-execution capabilities compatibly to
  `etlantic.orchestration/1`; or
- publish a narrowly scoped `etlantic.scheduler/1` protocol.

The decision must avoid two overlapping plugin discovery systems. Shared
models for retry intent, schedule intent, capabilities, correlation, and
reports should be reused. A protocol major is required if existing
orchestrator meaning cannot be extended compatibly.

## 0.15: scheduler extraction and hardening

This is a companion workstream to the mandatory 0.15 Safe SQL Lowering gate.
It must not delay that gate unless the SQL runtime requires a scheduler
correction for semantic safety.

Deliver:

- inventory the existing local runner's ETLantic-specific and generic
  responsibilities
- extract one scheduling boundary without changing public run semantics
- implement `LocalScheduler` through that boundary
- preserve `Pipeline.run()` and `Pipeline.arun()` behavior
- preserve plan fingerprints and serialized plan/report schemas
- formalize physical-unit readiness, completion, failure, cancellation, and
  timeout transitions
- make concurrency and retry limits explicit and bounded
- prevent scheduler code from reselecting implementations or plugins
- add scheduler capability analysis and structured diagnostics
- add private scheduler conformance fixtures
- document the direct-execution versus external-compilation distinction
- complete a Prefect adapter spike against the resolved physical-unit model

Non-goals for 0.15:

- shipping Prefect in core
- making Prefect the default
- requiring a Prefect server or Cloud account
- changing pipeline authoring
- exposing Prefect tasks, states, deployments, or configuration through the
  ETLantic public model
- replacing `etlantic-airflow`

Acceptance scenarios:

- existing local quickstarts and runtime suites produce equivalent results and
  reports through `LocalScheduler`
- two independent ready branches execute concurrently within a declared bound
- retries occur only when ETLantic's resolved retry-safety policy allows them
- cancellation and timeout produce stable ETLantic states and diagnostics
- partial runs preserve dependency closure and logical identities
- scheduler analysis performs no data access, secret resolution, or backend
  contact
- a scheduler cannot silently alter physical regions or implementation choices

Exit gate:

The built-in local path uses one explicit scheduler boundary, retains current
observable behavior, and passes the private conformance corpus. The Prefect
spike demonstrates feasibility without becoming a release dependency.

## 0.16: optional `etlantic-prefect`

After the 0.15 scheduler boundary is proven, publish
`etlantic-prefect` as the reference Python-native orchestration plugin.

Deliver:

- deterministic mapping from resolved ETLantic physical units to Prefect flows
  and tasks
- local direct invocation without requiring a deployment for the basic path
- optional deployment/serve integration behind Prefect-owned configuration
- exact capability declaration for concurrency, retries, cancellation,
  timeouts, schedules, and artifact transport
- stable mapping between ETLantic run/unit identities and Prefect flow/task-run
  identities
- ETLantic-owned output normalization and `PipelineRunReport`
- redacted diagnostics and event correlation
- no Prefect object in `PipelinePlan`, contracts, or portable transformation IR
- optional dependency/package installation only
- public scheduler/orchestrator conformance fixtures shared with
  `LocalScheduler` where behavior overlaps
- comparison documentation for local, Prefect, and Airflow paths

The plugin must not:

- decorate user transformations with Prefect APIs
- reconstruct or dynamically rediscover the logical pipeline
- reselect transformation, storage, dataframe, SQL, or Spark plugins
- pass datasets through a metadata channel intended only for small control
  payloads
- weaken ETLantic retry, transaction, validation, security, or materialization
  boundaries
- require Prefect Cloud for local execution

Acceptance scenarios:

- the same resolved plan executes locally and through Prefect with equivalent
  logical results, lifecycle states, and report shape
- independent physical units use the configured Prefect task runner without
  changing dependencies
- unsupported scheduling requirements fail during planning
- retries are not duplicated between ETLantic and Prefect
- large artifacts use declared artifact references rather than control-plane
  payloads
- secrets remain runtime-only and absent from plans, Prefect parameters,
  diagnostics, and reports
- production selection requires explicit profile configuration and plugin
  allowlisting

Exit gate:

`etlantic-prefect` passes the public conformance suite as an optional plugin;
`LocalScheduler` remains the default and `etlantic-airflow` remains the
reference external compiler.

## Default selection policy

| Context | Default or requirement |
|---|---|
| Development | built-in `LocalScheduler` |
| Tests | built-in `LocalScheduler` |
| Notebooks and embedded use | built-in `LocalScheduler` |
| Validation and planning CI | no execution scheduler required |
| Prefect execution | explicit `Profile(orchestrator="prefect")` |
| Airflow deployment | explicit compile target and `etlantic-airflow` |
| Production | explicit orchestrator plus non-empty plugin allowlist |

Unknown orchestrator names and missing plugins fail closed. The production
profile must not silently choose Prefect, Airflow, or local execution.

## Conformance requirements

The scheduler suite covers:

- capability accuracy
- dependency and concurrency behavior
- sync and async units
- retries and retry-safety enforcement
- cancellation, timeout, and abandoned work
- partial-run dependency closure
- callback and lifecycle ordering
- multiple output roles
- artifact ownership and transport
- logical identity correlation
- deterministic diagnostics
- result and report equivalence
- secret and row-data exclusion from control artifacts
- bounded hostile plans and failure behavior

Platform-specific capabilities run additional fixtures. Passing generic
dependency scheduling tests does not permit a plugin to claim durable
scheduling, event triggers, approvals, or distributed execution.

## Dependency and security policy

- Prefect remains an optional plugin dependency and never an ETLantic core
  dependency.
- Core imports must succeed without Prefect installed.
- Prefect discovery follows the existing entry-point trust boundary.
- Production profiles require allowlisting and compatible version policy.
- Plugin and Prefect versions appear in plan/execution evidence without secret
  values.
- ETLantic does not adopt unsafe serialization to satisfy a scheduler backend.
- Data artifacts remain outside scheduler control payloads unless explicitly
  bounded and safe.

## Documentation deliverables

- update the execution model with the scheduler/compiler distinction
- document `LocalScheduler` as the zero-service reference
- add an `etlantic-prefect` installation and execution guide when shipped
- retain Airflow as the external compilation guide
- add a local/Prefect/Airflow decision table
- document profile selection and production allowlisting
- publish migration notes only if observable local-runner behavior changes

## Final success criteria

The program succeeds when ETLantic has a smaller, testable built-in scheduling
kernel; an optional Prefect integration can coordinate the same resolved plans;
Airflow compilation remains independent; and no orchestrator becomes part of
ETLantic's logical authoring or portable semantic model.
