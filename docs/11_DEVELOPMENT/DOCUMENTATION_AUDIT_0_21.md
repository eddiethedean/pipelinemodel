# Documentation Audit — ETLantic 0.21

> Status: Maintained audit for the 0.21 documentation adoption cut.

## Verdict

Overall quality before this cut: **Fair**. Volume and honesty about limits were
strong; golden-path drift, factual errors, and security residual contradictions
undermined trust.

This audit documents the 0.21 remediation pass. See also
[Documentation Audit 0.20](DOCUMENTATION_AUDIT_0_20.md).

## Fixed in this cut

1. `SECURITY.md` supported-versions table (duplicate `0.21.x` row)
2. Root `SUPPORT.md` banner (`0.20.0` → `0.21.0`)
3. Troubleshooting plugin-minor advice (`0.21` requires matching `0.21` plugins)
4. README CLI default profile (`development`, not `local`)
5. Canonical Quickstart = `etlantic init`; README/docs home/Cookbook aligned
6. Quickstart success criteria (`succeeded` + `data/out.json`)
7. `examples/quickstart.py` → `examples/memory_customers.py` (relabeled)
8. First Pipeline extends the init project
9. Evaluator / Production Readiness / Security residual-risk matrix reconciled
10. Architecture plugin families: shipped vs Future design
11. Data Contracts Source/Sink → Extract/Load (primary pages)
12. README roadmap link → Roadmap summary
13. Issue templates refreshed to 0.21
14. `check_docs.py` gates for SUPPORT/SECURITY/golden-path regressions
15. Best Practices guide; contributor minimal first-PR path
16. Nav: historical What’s-new under Earlier releases

## Remaining debt

- Split long Security threat-model body vs shipped controls further if needed
- CLI.md contract test against Typer help
- Broader Source/Sink purge in deep VALIDATION / PYDANTIC chapters
- Search `noindex` for Design Proposal stubs
- Adopter performance page with current harness (retire 0.10 baselines)
- From-dbt/Airflow/Dagster migration cookbook

## Release gate

Before tagging a docs-impacting release:

- [ ] Root `SUPPORT.md` opening version == package version
- [ ] `SECURITY.md` support table has exactly one current-minor row
- [ ] Evaluator / Production Readiness / Security residual language agree
- [ ] `uv run python scripts/check_docs.py` passes
- [ ] Green path pages agree on `etlantic init` as Quickstart
