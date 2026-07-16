# Evaluator Brief

A one-page answer for enterprise evaluators and technical decision-makers.

## What Pipelantic is

A typed, contract-driven **modeling** layer for data pipelines in Python. You
define datasets, transformations, and pipelines once; Pipelantic validates and
plans them; plugins execute.

It is **not** a dataframe engine, distributed scheduler, warehouse, or secret
manager.

## What is ready in alpha 0.5.0

| Area | Ready? |
|---|---|
| Typed authoring (`Data`, `Transformation`, `Pipeline`) | Yes |
| Validation and secret-free `PipelinePlan` | Yes |
| ODCS / DTCS / DPCS interchange | Yes |
| Local in-process runtime + run reports | Yes |
| Memory / callable / JSON / CSV / no-write storage | Yes |
| Env + mounted-file secrets | Yes |
| Polars / Pandas plugins | Yes (separate packages) |
| SQL / Spark / Airflow | No — future design |
| Multi-tenant durable orchestration | No |
| Formal SLA / support response times | No |

## Security posture

- Plans never contain resolved secrets
- Threat model documents many controls as **Gap** (plugin allowlists, DoS
  budgets, stronger isolation)—read
  [Security](../02_FOUNDATIONS/SECURITY.md) and the repository
  [security policy](https://github.com/eddiethedean/pipelantic/blob/main/SECURITY.md)
- Report vulnerabilities privately; alpha has best-effort fixes only

## What not to bet on yet

- Copying long “design study” tutorials (SQL/Spark/Airflow) into production
- AWS Secrets Manager / Vault / keyring configuration from older docs
- Process-local reports as an audit system of record
- Stable 1.0 compatibility guarantees

## Recommended evaluation path

1. [Capabilities](CAPABILITIES.md)
2. [Quickstart](QUICKSTART.md) or `examples/quickstart.py`
3. Optional: `examples/dataframe_parity.py` with Polars or Pandas
4. [Migration 0.4 → 0.5](../11_DEVELOPMENT/MIGRATION_0_4_TO_0_5.md) if upgrading
5. [Roadmap](../11_DEVELOPMENT/ROADMAP.md) for sequencing

## Support channel

GitHub issues for bugs and questions. Include Pipelantic version, Python
version, and a minimal reproduction. Never include credentials or production
data.
