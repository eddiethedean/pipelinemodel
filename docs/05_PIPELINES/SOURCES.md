# Sources (removed)

`Source` was removed in ETLantic **0.16**. Use [`Extract`](EXTRACTS.md):

```python
from etlantic import Extract

customers = Extract[RawCustomer](asset="customers_csv")
```

See [Migration 0.15 → 0.16](../11_DEVELOPMENT/MIGRATION_0_15_TO_0_16.md).
