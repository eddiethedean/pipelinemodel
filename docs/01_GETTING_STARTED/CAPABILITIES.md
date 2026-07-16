# Current Capabilities and Limitations

Pipelantic 0.4.0 is an alpha release. This page is the shortest answer to
"What can I use today?"

## Available in 0.4

| Capability | Status |
|---|---|
| Typed data, transformation, and pipeline models | Available |
| Structural and semantic validation | Available |
| ODCS, DTCS, and DPCS generation and loading | Available |
| Profiles and deterministic, secret-free pipeline plans | Available |
| Local synchronous and asynchronous execution | Available |
| Python transformation implementations | Available |
| Memory, callable, JSON, CSV, and no-write storage | Available |
| Run reports, structured logging, and local debugging | Available |
| Runtime secret references and env/file providers | Available |

## Not included in 0.4

| Capability | Status |
|---|---|
| Pandas or Polars execution plugins | Future design |
| SQL compilation or execution | Future design |
| PySpark or streaming execution | Future design |
| Airflow or other orchestrator compilation | Future design |
| Public third-party Plugin SDK | Future design |
| Graphviz and generated HTML pipeline documentation | Future design |
| Stable 1.0 compatibility guarantees | Not yet |

Pages describing unavailable capabilities are retained as design material.
They are not evidence that an API or plugin has shipped.

## Production Readiness

Pipelantic is suitable for evaluation, prototypes, contract generation, plan
inspection, and controlled local execution. It should not yet be treated as a
production orchestration platform or as a stable replacement for a dataframe,
SQL, Spark, or scheduling engine.

Before production use, evaluate the alpha stability policy, security model,
storage semantics, failure behavior, and compatibility requirements for your
environment.
