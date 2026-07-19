# Migration 0.13 → 0.14

ETLantic **0.14.0** adds portable Pandas compilation and publishes the portable
transform compiler conformance suite. Polars and PySpark relational claims from
0.13 remain available.

## Install

Pin core and every official plugin to 0.14.0:

```bash
pip install --upgrade \
  'etlantic==0.14.0' \
  'etlantic-polars==0.14.0' \
  'etlantic-pandas==0.14.0' \
  'etlantic-pyspark==0.14.0'
```

Install only the engine packages your pipeline uses. Extras resolve their
official plugins at `==0.14.0`.

## What changed

| Area | 0.13 | 0.14 |
|---|---|---|
| Pandas portable compiler | Not available | Kernel + `portable-relational/1`, eager and index-neutral |
| Public compiler conformance | Deferred | Available through `etlantic.testing` |
| Reference-engine coverage | Polars + PySpark | Polars + PySpark + Pandas |
| Differential CI | Two engines | Three engines |

Pandas pipelines using `portable_transform_policy="require"` can now compile
without `@implementation("pandas")` when the portable plan fits the compiler's
claims. Unsupported lazy, type, action, function, or semantic modes continue to
fail closed during planning.

## Third-party compiler action

Run the public suite against the compiler object:

```python
from etlantic.testing import run_portable_transform_conformance_suite

run_portable_transform_conformance_suite(create_transform_compiler())
```

The suite selects fixtures from the exact profiles, actions, and functions the
compiler advertises. Remove unsupported claims or fix their semantics before
releasing the plugin.

Pin the suite and core to the ETLantic minor your plugin certifies against.
Continue to fail closed from `analyze()` for unsupported modes, and keep plans,
diagnostics, and explain payloads secret-free.

## Upgrade checklist

1. Upgrade core and official plugins together to `==0.14.0`.
2. Re-plan portable pipelines and inspect the selected compiler and support
   summary.
3. Run the portable conformance suite for each third-party compiler.
4. Run application-level differentials for the engines your project supports.
5. Retain native implementations for capabilities outside kernel +
   `portable-relational/1`.

## Documentation and navigation

- Start with [What's New in 0.14](../01_GETTING_STARTED/WHATS_NEW_0_14.md) for
  the adopter-facing release summary.
- Treat [Capabilities](../01_GETTING_STARTED/CAPABILITIES.md) as the current
  shipped boundary.
- Use [Portable Transformations](../04_TRANSFORMATIONS/PORTABLE_TRANSFORMATIONS.md)
  for supported semantics and [Testing Plugins](../07_PLUGIN_SDK/TESTING_PLUGINS.md)
  for the public suite.
- Replace links to the 0.11 → 0.12 migration as the latest upgrade path with
  this guide. Keep older migration pages for historical upgrades.

Review the complete [0.14 changelog](https://github.com/eddiethedean/etlantic/blob/main/CHANGELOG.md#0140---2026-07-18).
