"""Public exception hierarchy for Pipelantic."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pipelantic.diagnostics import ValidationReport


class PipelanticError(Exception):
    """Base class for public Pipelantic exceptions."""


class ModelDefinitionError(PipelanticError):
    """Raised when a class definition cannot form a usable model."""


class PipelineValidationError(PipelanticError):
    """Raised when validation fails and the caller requested an exception."""

    def __init__(self, message: str, *, report: ValidationReport) -> None:
        super().__init__(message)
        self.report = report


class InternalPipelanticError(PipelanticError):
    """Raised when an internal invariant is violated."""
