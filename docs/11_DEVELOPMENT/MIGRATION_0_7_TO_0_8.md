# Migrating from 0.7 to 0.8

ETLantic 0.8 adds **external orchestration**: a versioned orchestrator
compilation protocol and an independently installable Airflow reference
compiler. Existing local, dataframe, SQL, and Spark paths remain compatible.

## What changed

- New protocol `etlantic.orchestration/1` under `etlantic.orchestration`
- Public API: `compile_plan(plan, target="airflow")` and
  `PipelinePlan.compile(target=...)`
- Package `etlantic-airflow` (entry point `etlantic.orchestrator_plugins`)
- `Profile.schedule`, `Profile.execution`, and
  `Profile.required_orchestrator_capabilities`
- Plugin packages bump to `0.8.0` and require `etlantic>=0.8.0,<0.9`

## Install

```bash
pip install --upgrade 'etlantic>=0.8.0'
pip install etlantic-airflow
# or: pip install 'etlantic[airflow]'
```

Core remains free of `apache-airflow`. Install Airflow only in environments
that import generated DAG modules.

## Authoring pattern

```python
from etlantic import Profile, plan_pipeline, compile_plan

profile = Profile(
    name="airflow",
    orchestrator="airflow",
    schedule={"type": "cron", "expression": "0 2 * * *", "timezone": "UTC"},
    execution={"retries": 1, "retry_delay_seconds": 60},
)
plan = plan_pipeline(MyPipeline, profile=profile)
artifact = compile_plan(plan, target="airflow", profile=profile)
artifact.write("dags/my_pipeline.py")
```

The same pipeline can still run locally with `orchestrator="local"`.

## Semantics to watch

- Retries on non-retry-safe sinks fail compilation (`PMORCH310`)
- Event schedules require sensors and fail closed in the 0.8 reference compiler
  (`PMORCH320`)
- Task boundaries carry durable `ArtifactRef` payloads only — not inline rows
- Generated DAG modules must remain secret-free (same rule as plans/reports)

## Unchanged

- Spark batch via `etlantic-pyspark` (streaming still experimental)
- SQL / Polars / Pandas plugins
- Local orchestrator default

## See also

- [Current Capabilities](../01_GETTING_STARTED/CAPABILITIES.md)
- [Airflow](../06_EXECUTION/AIRFLOW.md)
- [CHANGELOG](https://github.com/eddiethedean/etlantic/blob/main/CHANGELOG.md)
