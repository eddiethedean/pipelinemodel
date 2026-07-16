"""Pipelantic — typed, contract-driven data pipeline modeling.

0.1 provides the authoring model, logical graph construction, topology and
compatibility diagnostics, inspection, and Mermaid output.

Data contracts are provided by ContractModel. This package re-exports
``DataContractModel`` as an alias of ``contractmodel.ContractModel`` for
documentation-aligned imports.
"""

from pipelantic._version import __version__
from pipelantic.contracts import DataContractModel
from pipelantic.diagnostics import Diagnostic, Severity, ValidationReport
from pipelantic.exceptions import (
    ModelDefinitionError,
    PipelanticError,
    PipelineValidationError,
)
from pipelantic.model import Edge, LogicalGraph, Node, NodeKind
from pipelantic.pipeline import Pipeline, Sink, Source, SubpipelineInstance
from pipelantic.ports import Input, Output, Parameter
from pipelantic.refs import OutputRef
from pipelantic.transformation import ImplementationRecord, Step, Transformation

__all__ = [
    "DataContractModel",
    "Diagnostic",
    "Edge",
    "ImplementationRecord",
    "Input",
    "LogicalGraph",
    "ModelDefinitionError",
    "Node",
    "NodeKind",
    "Output",
    "OutputRef",
    "Parameter",
    "PipelanticError",
    "Pipeline",
    "PipelineValidationError",
    "Severity",
    "Sink",
    "Source",
    "Step",
    "SubpipelineInstance",
    "Transformation",
    "ValidationReport",
    "__version__",
]
