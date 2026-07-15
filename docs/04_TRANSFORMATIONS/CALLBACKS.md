# Callbacks

Callbacks allow applications to respond to important events in a pipeline's lifecycle
without embedding operational logic inside transformation implementations.

PipelineModel coordinates callback invocation. Execution plugins perform the
underlying work.

## Goals

Callbacks should:

- Separate business logic from operational behavior.
- Support synchronous and asynchronous functions.
- Be strongly typed.
- Be execution-engine independent.
- Produce predictable, inspectable behavior.

## Callback Types

Typical callback categories include:

- Invalid input data
- Invalid output data
- Transformation failure
- Retry decisions
- Transformation completion
- Pipeline completion
- Pipeline failure

## Invalid Data

```python
from pipelinemodel import (
    InvalidDataAction,
    InvalidDataContext,
    on_invalid_data,
)

@on_invalid_data
def quarantine(context: InvalidDataContext[Customer]) -> InvalidDataAction:
    return InvalidDataAction.quarantine(
        destination="invalid-customers",
        continue_with_valid=True,
    )
```

PipelineModel interprets the returned action while the execution plugin performs
the quarantine or filtering.

## Failure Callbacks

```python
from pipelinemodel import FailureContext, on_failure

@on_failure
def notify(context: FailureContext):
    ...
```

Failure callbacks may:

- Log diagnostics
- Send notifications
- Trigger incident workflows
- Decide retry behavior

## Completion Callbacks

```python
from pipelinemodel import CompletionContext, on_complete

@on_complete
async def publish_metrics(context: CompletionContext):
    ...
```

Completion hooks are useful for metrics, auditing, and downstream automation.

## Sync and Async

Callbacks may use either style.

```python
@on_failure
def handler(context):
    ...
```

```python
@on_failure
async def handler(context):
    ...
```

PipelineModel normalizes invocation internally.

## Typed Context Objects

Callbacks receive strongly typed context objects rather than unstructured
dictionaries.

Typical context information includes:

- Pipeline identifier
- Transformation identifier
- Contract identity
- Execution profile
- Run identifier
- Diagnostics
- Exception information (when applicable)

## Callback Actions

Some callbacks return an action object.

Conceptually:

```python
return InvalidDataAction.fail()
return InvalidDataAction.retry()
return InvalidDataAction.quarantine(...)
return InvalidDataAction.continue_with_valid()
```

The action remains declarative. Plugins execute the requested behavior.

## Ordering

When multiple callbacks are registered, PipelineModel should execute them in a
deterministic order documented by the framework.

## Best Practices

- Keep callbacks focused on operational concerns.
- Use typed context objects.
- Avoid modifying pipeline topology from callbacks.
- Prefer declarative action objects over side effects.
- Keep callbacks idempotent where practical.

## Anti-Patterns

Avoid:

- Embedding business transformations inside callbacks.
- Depending on runtime-specific objects.
- Mutating contracts.
- Swallowing failures silently.

## Key Principle

> Callbacks describe **how the framework should respond** to lifecycle events.
> They do not change the logical transformation contract.

## Next Step

Continue with **VALIDATION.md** to learn how PipelineModel validates
transformations before and during execution.
