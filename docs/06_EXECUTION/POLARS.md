# Polars Plugin

**Status: shipped in 0.5.0** as the reference dataframe backend
(`etlantic-polars`).

The portable transformation compiler described below is planned for 0.12 and
is not part of the current 0.11 plugin.

## Install

```bash
pip install etlantic-polars
pip install 'etlantic-polars[arrow]'  # optional
```

## Behavior

- Eager `DataFrame` execution is the baseline
- `LazyFrame` values are preserved across adjacent Polars steps
- Collection happens only at plan-declared boundaries (sink publication,
  cross-engine conversion, explicit collection points)
- Contract ↔ Polars dtype mapping with structured diagnostics for unsupported
  types
- Sync and async implementation callables are supported

## Portable compiler (planned 0.12)

The Polars compiler is the first planned executable lowering for
`dtcs.transform-plan/2` (v1 readable). In **0.12** it claims **only**
`dtcs:profile/portable-relational-kernel/1` (plan-v2 `/2` metadata
compatibility without extra relational ops). Join, union, group, aggregate,
sort, distinct, and limit **execution** claims land in **0.13**. It will:

- lower portable kernel columns to native `pl.Expr` values
- lower kernel relational nodes to `DataFrame` and `LazyFrame` operations
- preserve `LazyFrame` across compatible portable steps
- reject unsupported (non-kernel) semantics during planning
- retain logical expression and output mappings
- collect only at plan-declared boundaries

It must not fall back to Python row functions or collect data to emulate an
unsupported operation. Richer authored profiles still need a native
`@implementation("polars")` (or a later compiler claim) until 0.13–0.15.

## Example

See `examples/dataframe_parity.py` in the repository:

```bash
uv run --group dataframes python examples/dataframe_parity.py polars
```
