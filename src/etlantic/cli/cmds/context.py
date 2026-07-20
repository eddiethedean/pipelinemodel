"""Shared CLI context and emit helpers."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import typer

from etlantic.lifecycle.runtime import PipelineRuntime


def emit_payload(data: Any, *, fmt: str) -> None:
    if fmt == "sarif" and isinstance(data, dict) and "runs" in data:
        typer.echo(json.dumps(data, indent=2, sort_keys=True))
        return
    if fmt == "json":
        typer.echo(json.dumps(data, indent=2, sort_keys=True, default=str))
        return
    if isinstance(data, dict):
        for key, value in data.items():
            typer.echo(f"{key}: {value}")
    else:
        typer.echo(str(data))


def report_to_payload(report: Any) -> dict[str, Any]:
    return {
        "valid": report.valid,
        "diagnostics": [
            {
                "code": d.code,
                "severity": d.severity.value,
                "message": d.message,
                "path": list(d.path),
                "phase": d.phase,
            }
            for d in report.diagnostics
        ],
    }


@dataclass
class CliContext:
    """Shared CLI dependencies."""

    load_target: Any
    runtime: PipelineRuntime
