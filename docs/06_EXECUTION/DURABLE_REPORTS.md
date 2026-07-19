# Durable Run Reports

`PipelineRuntime` uses an in-memory `ReportStore` by default. Use the shipped
`FileReportStore` when reports must survive process boundaries.

## Persist reports during execution

In 0.14.0, `FileReportStore` lives in `etlantic.reports.file_store`; it is not
re-exported from the `etlantic.reports` package root.

```python
from pathlib import Path

from etlantic import PipelineRuntime
from etlantic.reports.file_store import FileReportStore
from package.pipeline import CustomerPipeline

store = FileReportStore(Path(".etlantic/reports"))
runtime = PipelineRuntime(reports=store)

report = CustomerPipeline.run(profile="development", runtime=runtime)
assert store.get(report.run_id) is not None
```

The store creates its root directory and writes one JSON file per `run_id`.
On construction it reloads valid `*.json` reports from that directory. Invalid
or unrelated JSON files are skipped. `get()` and `list()` then use the
process-local index populated from disk.

You can also persist a report explicitly:

```python
store.put(report)
recent = store.list(pipeline_id=report.pipeline_id, limit=10)
```

Choose a directory with appropriate access control. Reports are designed to be
secret-free, but they can contain pipeline identities, diagnostics, artifact
references, and operational metadata.

## CLI process boundaries

The CLI runtime's default report store is process-local. A report created by:

```bash
etlantic run package.pipeline:CustomerPipeline --profile development
```

is not available to a later `etlantic report show` or `report export` process.
Those commands do not automatically discover `.etlantic/reports`. Persist from
Python with `PipelineRuntime(reports=FileReportStore(...))`, or export the
report JSON as part of the process that produced it.

## Compare persisted reports

The Python comparison helper reports status, step-status, plan-fingerprint,
and artifact-count differences:

```python
from etlantic.reports.file_store import FileReportStore, compare_reports

store = FileReportStore(".etlantic/reports")
left = store.get("run-left")
right = store.get("run-right")
if left is None or right is None:
    raise LookupError("report not found")

comparison = compare_reports(left, right)
print(comparison)
```

The CLI can compare run IDs from a file store:

```bash
etlantic report compare run-left run-right \
  --store .etlantic/reports --format json
```

It can also compare two report JSON paths without `--store`:

```bash
etlantic report compare reports/before.json reports/after.json --format json
```

See [Run Reports](RUN_REPORTS.md), [Logging](LOGGING.md), and
[Pilot Walkthrough](PILOT_WALKTHROUGH.md).
