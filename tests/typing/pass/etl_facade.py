"""Positive typing fixture: curated ``import etlantic as etl`` facade."""

from __future__ import annotations

import etlantic as etl
from etlantic import Data, Pipeline, Profile


class Customer(etl.Data):
    customer_id: int
    name: str


def _uses_namespaces() -> None:
    _ = etl.sql
    _ = etl.testing
    _ = etl.dataframe
    plan_fn = etl.plan_pipeline
    assert callable(plan_fn)
    assert issubclass(Customer, Data)
    assert issubclass(etl.Pipeline, Pipeline)
    assert Profile is etl.Profile
