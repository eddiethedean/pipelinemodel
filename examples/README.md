# Runnable Examples

These examples use only APIs and dependencies shipped in Pipelantic 0.4.

## Quickstart

```bash
python examples/quickstart.py
```

The example defines contracts, registers a local Python implementation, runs
the pipeline with in-memory storage, prints the run report, and prints the
curated records.

## JSON and CSV storage

`file_storage.py` contains tested `json_to_json()` and `csv_to_csv()` workflows
using built-in storage bindings and an explicit planning context.

Documentation pages for Pandas, Polars, SQL, Spark, Airflow, and other future
plugins are design material and are not runnable examples for the current
release.
