# Troubleshooting

## `pip install pipelantic` rejects my Python version

Pipelantic requires Python 3.11 or newer. Check with:

```bash
python --version
```

## A transformation has no implementation

Declaring a `Transformation` defines its contract, not its executable code.
Register a local implementation before running:

```python
@MyTransformation.implementation("local")
def run_locally(rows):
    return rows
```

## My memory source returns no records

Seed the exact binding name used by the pipeline:

```python
runtime.memory.seed("customer_source", records)
```

Read sink output using its binding:

```python
runtime.memory.get("customer_sink")
```

## Planning and execution use different profiles

Use `local` for plan-oriented examples or `development` for the built-in local
runtime examples. Do not silently switch profile names within one workflow.

## A Pandas, Polars, SQL, Spark, or Airflow example fails

Those integrations are design material in 0.4 and are not shipped plugins.
Start with the runnable examples under `examples/`.

## Commands in a design page do not exist

The current CLI supports `validate`, `inspect`, `plan`, `plan explain`, `run`,
and `report show|export`. See the [CLI reference](../10_REFERENCE/CLI.md).

## A virtual environment breaks after moving the repository

Virtual-environment entry points contain absolute paths. Delete and recreate
the environment after moving or renaming a checkout:

```bash
rm -rf .venv
uv sync --locked
```

Only run the removal command from the repository root after confirming
`.venv` is the project environment.

## Where to report a problem

Include the Pipelantic version, Python version, command, complete traceback or
diagnostic code, and a minimal pipeline definition in the issue report. Never
include credentials or production data.
