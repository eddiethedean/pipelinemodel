"""Package import smoke tests."""

import pipelantic


def test_version() -> None:
    assert pipelantic.__version__ == "0.1.0"


def test_root_exports() -> None:
    assert hasattr(pipelantic, "Pipeline")
    assert hasattr(pipelantic, "Transformation")
    assert hasattr(pipelantic, "Input")
    assert hasattr(pipelantic, "Output")
    assert hasattr(pipelantic, "Parameter")
    assert hasattr(pipelantic, "Source")
    assert hasattr(pipelantic, "Sink")
    assert hasattr(pipelantic, "OutputRef")
    assert hasattr(pipelantic, "DataContractModel")
