# Known Limitations

- The project is alpha and does not promise 1.0 API stability.
- Local execution is in-process; Pipelantic is not a distributed scheduler.
- Pandas, Polars, SQL, Spark, Airflow, and other external backend plugins are
  not included in 0.4.
- Many design pages describe intended 1.0 behavior. Check the page status
  before copying code.
- Process-local report history is not a durable report database.
- In-memory storage is intended for local development and tests.
- Generated plans should be regenerated after incompatible schema changes
  rather than edited by hand.

Release-specific fixes and changes are recorded in the
[changelog](https://github.com/eddiethedean/pipelantic/blob/main/CHANGELOG.md).
