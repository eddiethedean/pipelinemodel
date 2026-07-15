# Resource Provider

A **Resource Provider** implements the PipelineModel Resource Provider API,
supplying runtime infrastructure services to execution plugins and
transformations.

Unlike storage plugins, which persist datasets, resource providers expose
operational services such as database connections, secret managers, HTTP
clients, caches, message brokers, ML endpoints, and compute resources.

Pipeline authors declare logical resource requirements. Resource providers
resolve those requirements into concrete runtime objects.

## Purpose

A resource provider is responsible for:

- Resolving logical resources
- Creating resource instances
- Managing authentication
- Managing lifecycle
- Pooling and reuse
- Health checks
- Structured diagnostics

It is **not** responsible for:

- Pipeline planning
- Pipeline orchestration
- Transformation semantics
- Data persistence
- Contract generation

## Architecture

```text
Pipeline Plan
      │
      ▼
Resource Provider API
      │
 ┌────┼───────────────────────────────┐
 ▼    ▼          ▼         ▼          ▼
SQL  Secrets    Redis     HTTP     Kafka
```

Resource providers supply services to other plugins while remaining independent
of the pipeline model.

## Declaring Resources

Conceptually:

```python
class NormalizeCustomers(Transformation):
    warehouse: Resource[SqlDatabase]
    cache: Resource[Redis]
```

The transformation depends on abstract resource types rather than vendor SDKs.

## Resolution

Execution profiles bind logical resources to implementations.

Development:

```text
warehouse -> SQLite
```

Production:

```text
warehouse -> PostgreSQL
```

No pipeline code changes are required.

## Provider Interface

Conceptually:

```python
class ResourceProvider:
    name: str
    version: str

    def resolve(self, resource_type, binding, context):
        ...
```

Providers may expose richer APIs, but all should resolve logical resources into
usable runtime objects.

## Lifecycle

Typical lifecycle:

```text
Discover
   │
Resolve
   │
Create
   │
Inject
   │
Use
   │
Dispose
```

Providers should clean up resources deterministically.

## Async Support

Providers should support both synchronous and asynchronous acquisition where
appropriate.

PipelineModel normalizes invocation so users do not manage event loops or
resource wiring.

## Capabilities

Providers should advertise capabilities such as:

- Async support
- Connection pooling
- Transactions
- Health monitoring
- Retry support
- Streaming
- High availability

Planning validates mandatory capabilities before execution.

## Error Handling

Providers should translate infrastructure-specific exceptions into structured
PipelineModel diagnostics containing:

- Resource identity
- Pipeline identity
- Step identity
- Provider details
- Original exception
- Suggested remediation

## Best Practices

- Depend on abstract resource types.
- Resolve resources through execution profiles.
- Keep credentials external.
- Reuse pooled resources.
- Dispose of resources predictably.

## Anti-Patterns

Avoid:

- Creating SDK clients directly inside transformations.
- Hard-coding credentials.
- Using global mutable singletons.
- Exposing provider-specific objects through public contracts.

## Key Principle

> A Resource Provider supplies runtime infrastructure services while keeping
> pipelines, transformations, and contracts independent of deployment
> environments and vendor SDKs.

## Next Step

Continue with **REGISTRY_PROVIDER.md** to learn how PipelineModel discovers,
publishes, and resolves portable contract artifacts.
