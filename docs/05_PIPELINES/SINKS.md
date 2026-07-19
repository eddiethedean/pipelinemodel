# Sinks (removed)

`Sink` was removed in ETLantic **0.16**. Use [`Load`](LOADS.md):

```python
from etlantic import Load

curated = Load[Customer](input=normalized.result, asset="customers_curated")
```

See [Migration 0.15 → 0.16](../11_DEVELOPMENT/MIGRATION_0_15_TO_0_16.md).
