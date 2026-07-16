# Compatibility Matrix

This table describes the declared compatibility of Pipelantic 0.4.0.

| Surface | Supported range or version |
|---|---|
| Python | 3.11, 3.12, 3.13 |
| Pydantic | `>=2.12,<3` |
| ContractModel | `>=0.1.2` |
| DTCS toolkit | `>=0.11,<1` |
| DPCS toolkit | `>=0.13,<1` |
| Pipeline plan schema | `pipelantic.plan/1` |
| Package stability | Alpha |
| Plugin SDK stability | Not published as a stable SDK |

The package metadata in `pyproject.toml` is authoritative for dependency
ranges. During the 0.x series, public APIs and persistent formats may change.
Breaking changes must be called out in the changelog with an upgrade path.
