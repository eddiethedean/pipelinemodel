# Migration 0.12 → 0.13

ETLantic **0.13.0** expands portable compilation from the Polars kernel to
kernel + `portable-relational/1` on Polars and PySpark.

## Install

For a historical 0.13 environment, pin core and plugins exactly:

```bash
pip install \
  'etlantic==0.13.0' \
  'etlantic-polars==0.13.0' \
  'etlantic-pyspark==0.13.0'
```

Official plugins must use the same release as core. For a new evaluation,
prefer 0.14 and follow [Migration 0.13 → 0.14](MIGRATION_0_13_TO_0_14.md).

## What changed

| Area | 0.12 | 0.13 |
|---|---|---|
| Polars compiler | Kernel profile | Kernel + `portable-relational/1` |
| PySpark compiler | Not available | Kernel + `portable-relational/1` |
| Relational actions | Native implementation required | Join, union, aggregate, sort, distinct, deduplicate, and limit |
| Public portable compiler conformance | Not available | Still deferred |

Portable relational plans that failed under
`portable_transform_policy="require"` in 0.12 can compile in 0.13 when they fit
the advertised Polars or PySpark claim.

## Breaking and behavioral notes

- Join `collisionPolicy` now fails closed to `fail` only. Suffix and coalesce
  behavior is not supported; rename or project colliding columns explicitly.
- PySpark portable compilation does not introduce automatic Python or Pandas
  UDF fallback. Keep a native `@implementation("pyspark")` for UDFs and
  unclaimed profiles.
- PySpark joins with unequal key names drop the right key column to match the
  portable semantics.
- `with_fields` replaces an existing PySpark column instead of duplicating it.
- Polars `unionByName` aligns columns by name and can fill missing columns only
  when that mode is explicitly allowed.
- Semi and anti joins ignore overlap in non-key right-side columns because
  their result contains only the left interface.
- PySpark `substr` uses zero-based portable offsets, and `replace` is literal.
- Windowed `with_fields` and positional union with
  `allowMissingColumns` fail analysis as unsupported modes.

Re-plan pipelines after upgrading so compiler identities, requirements, and
support findings reflect 0.13.

## Conformance in 0.13

There is no public
`etlantic.testing.portable_transform_conformance` suite in 0.13. The release
uses repository-private differential fixtures. Third-party compiler authors
should not treat those private tests as a public compatibility contract.

The public suite ships in 0.14; upgrade and run it before advertising compiler
claims.

## See also

- [Portable Transformations](../04_TRANSFORMATIONS/PORTABLE_TRANSFORMATIONS.md)
- [Capabilities](../01_GETTING_STARTED/CAPABILITIES.md)
- [Migration 0.13 → 0.14](MIGRATION_0_13_TO_0_14.md)
- [0.13 changelog](https://github.com/eddiethedean/etlantic/blob/main/CHANGELOG.md#0130---2026-07-18)
