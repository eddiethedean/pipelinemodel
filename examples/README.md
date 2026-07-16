# Runnable Examples

These examples use only APIs and dependencies shipped in Pipelantic 0.5.

## Quickstart

```bash
python examples/quickstart.py
```

The example defines contracts, registers a local Python implementation, runs
the pipeline with in-memory storage, prints the run report, and prints the
curated records.

## JSON and CSV storage

```bash
python examples/file_storage.py
```

Runs tested `json_to_json()` and `csv_to_csv()` workflows using built-in
storage bindings.

## Dataframe parity (Polars / Pandas)

```bash
# requires pipelantic-polars / pipelantic-pandas
python examples/dataframe_parity.py polars
python examples/dataframe_parity.py pandas
```

Runs the same logical pipeline against either dataframe plugin via
`Profile.dataframe_engine`.

Documentation pages for SQL, Spark, Airflow, and other future plugins are
design material and are not runnable examples for the current release.
