"""Structural validation for the 0.1 modeling kernel."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pipelantic.contracts import is_data_contract_type
from pipelantic.diagnostics import Diagnostic, Severity, ValidationReport
from pipelantic.identity import contract_id, published_contract_id
from pipelantic.model import LogicalGraph
from pipelantic.transformation import Step, Transformation

if TYPE_CHECKING:
    from pipelantic.pipeline import Pipeline


def validate_pipeline(pipeline_cls: type[Pipeline]) -> ValidationReport:
    """Validate a pipeline definition and return a structured report."""
    diagnostics: list[Diagnostic] = []
    diagnostics.extend(_validate_member_definitions(pipeline_cls))
    diagnostics.extend(_validate_nested_subpipelines(pipeline_cls))
    graph = pipeline_cls.build_graph()
    build_error = getattr(pipeline_cls, "_graph_build_error", None)
    if build_error:
        diagnostics.append(
            Diagnostic(
                code="PMPIPE302",
                severity=Severity.ERROR,
                message=build_error,
                path=("pipeline",),
            )
        )
    diagnostics.extend(_validate_graph(graph, pipeline_cls))
    diagnostics.extend(_validate_port_compatibility(graph, pipeline_cls))
    return ValidationReport.from_diagnostics(diagnostics)


def _validate_nested_subpipelines(pipeline_cls: type[Pipeline]) -> list[Diagnostic]:
    """Recursively validate embedded subpipeline definitions."""
    from pipelantic.pipeline import SubpipelineInstance

    diagnostics: list[Diagnostic] = []
    for name, member in pipeline_cls.__pipeline_members__.items():
        if not isinstance(member, SubpipelineInstance):
            continue
        child_report = validate_pipeline(member.pipeline_cls)
        for diagnostic in child_report.diagnostics:
            diagnostics.append(
                Diagnostic(
                    code=diagnostic.code,
                    severity=diagnostic.severity,
                    message=diagnostic.message,
                    path=("pipeline", name, *diagnostic.path),
                    help=diagnostic.help,
                    related=diagnostic.related,
                    source=diagnostic.source,
                    metadata={**diagnostic.metadata, "subpipeline": name},
                )
            )
    return diagnostics


def _validate_member_definitions(pipeline_cls: type[Pipeline]) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    members = pipeline_cls.__pipeline_members__

    for name, member in members.items():
        if isinstance(member, Step):
            transform = member.transformation
            for problem in transform.validate_definition():
                diagnostics.append(
                    Diagnostic(
                        code="PMTRN001",
                        severity=Severity.ERROR,
                        message=problem,
                        path=("pipeline", name),
                    )
                )
            for port in transform.inputs():
                if port.name not in member.bindings:
                    diagnostics.append(
                        Diagnostic(
                            code="PMTRN101",
                            severity=Severity.ERROR,
                            message=(
                                f'Step "{name}" is missing required input '
                                f'"{port.name}".'
                            ),
                            path=("pipeline", name, port.name),
                            help=(
                                "Pass the input when calling Transformation.step(...)."
                            ),
                        )
                    )
                else:
                    diagnostics.extend(
                        _validate_binding_present(
                            member.bindings[port.name],
                            consumer=("pipeline", name, port.name),
                        )
                    )
                if port.contract_type is not None and not is_data_contract_type(
                    port.contract_type
                ):
                    diagnostics.append(
                        Diagnostic(
                            code="PMDATA101",
                            severity=Severity.ERROR,
                            message=(
                                f'Input "{port.name}" on {transform.__name__} '
                                f"does not reference a ContractModel type."
                            ),
                            path=("transformation", transform.__name__, port.name),
                        )
                    )
            for port in transform.outputs():
                if port.contract_type is not None and not is_data_contract_type(
                    port.contract_type
                ):
                    diagnostics.append(
                        Diagnostic(
                            code="PMDATA102",
                            severity=Severity.ERROR,
                            message=(
                                f'Output "{port.name}" on {transform.__name__} '
                                f"does not reference a ContractModel type."
                            ),
                            path=("transformation", transform.__name__, port.name),
                        )
                    )
            for port in transform.parameters():
                if not port.has_default and port.name not in member.parameters:
                    diagnostics.append(
                        Diagnostic(
                            code="PMTRN102",
                            severity=Severity.ERROR,
                            message=(
                                f'Step "{name}" is missing required parameter '
                                f'"{port.name}".'
                            ),
                            path=("pipeline", name, port.name),
                        )
                    )

        elif hasattr(member, "contract_type"):
            ctype = member.contract_type
            if ctype is not None and not is_data_contract_type(ctype):
                diagnostics.append(
                    Diagnostic(
                        code="PMDATA103",
                        severity=Severity.ERROR,
                        message=(
                            f'Node "{name}" contract type is not a ContractModel '
                            f"subclass."
                        ),
                        path=("pipeline", name),
                    )
                )

    return diagnostics


def _validate_binding_present(
    value: Any, *, consumer: tuple[str, ...]
) -> list[Diagnostic]:
    if value is None:
        return [
            Diagnostic(
                code="PMPIPE201",
                severity=Severity.ERROR,
                message="Input binding is missing.",
                path=consumer,
            )
        ]
    return []


def _validate_graph(
    graph: LogicalGraph, pipeline_cls: type[Pipeline]
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    names = [node.name for node in graph.nodes]
    seen: set[str] = set()
    for name in names:
        if name in seen:
            diagnostics.append(
                Diagnostic(
                    code="PMPIPE110",
                    severity=Severity.ERROR,
                    message=f'Duplicate node identity "{name}".',
                    path=("pipeline", name),
                )
            )
        seen.add(name)

    node_names = set(names)
    for edge in graph.edges:
        if edge.producer_node not in node_names:
            diagnostics.append(
                Diagnostic(
                    code="PMPIPE201",
                    severity=Severity.ERROR,
                    message=(
                        f'Unknown producer "{edge.producer_node}" wired to '
                        f'"{edge.consumer_node}.{edge.consumer_port}".'
                    ),
                    path=("pipeline", edge.consumer_node, edge.consumer_port),
                    related=(("pipeline", edge.producer_node),),
                )
            )
        if edge.consumer_node not in node_names:
            diagnostics.append(
                Diagnostic(
                    code="PMPIPE201",
                    severity=Severity.ERROR,
                    message=f'Unknown consumer "{edge.consumer_node}".',
                    path=("pipeline", edge.consumer_node),
                )
            )

    # Missing edge for required step inputs already covered; also detect
    # unresolved refs where binding existed but no edge was created.
    members = pipeline_cls.__pipeline_members__
    edge_keys = {(e.consumer_node, e.consumer_port) for e in graph.edges}
    for name, member in members.items():
        if isinstance(member, Step):
            for port in member.transformation.inputs():
                if port.name in member.bindings and (name, port.name) not in edge_keys:
                    diagnostics.append(
                        Diagnostic(
                            code="PMPIPE201",
                            severity=Severity.ERROR,
                            message=(
                                f'Could not resolve input "{port.name}" on step '
                                f'"{name}".'
                            ),
                            path=("pipeline", name, port.name),
                            help="Bind a Source, Step output, or OutputRef.",
                        )
                    )
        from pipelantic.pipeline import Sink, SubpipelineInstance

        if isinstance(member, Sink) and (name, "input") not in edge_keys:
            diagnostics.append(
                Diagnostic(
                    code="PMPIPE201",
                    severity=Severity.ERROR,
                    message=f'Could not resolve input for sink "{name}".',
                    path=("pipeline", name, "input"),
                )
            )
        if isinstance(member, SubpipelineInstance):
            node = graph.node_map().get(name)
            public_inputs = {p.name for p in node.inputs} if node else set()
            for port_name in member.bindings:
                if port_name not in public_inputs:
                    diagnostics.append(
                        Diagnostic(
                            code="PMPIPE201",
                            severity=Severity.ERROR,
                            message=(
                                f'Unknown subpipeline input "{port_name}" on "{name}".'
                            ),
                            path=("pipeline", name, port_name),
                            help=(
                                "Bind only public source ports exposed by the "
                                "child pipeline."
                            ),
                        )
                    )
                elif (name, port_name) not in edge_keys:
                    diagnostics.append(
                        Diagnostic(
                            code="PMPIPE201",
                            severity=Severity.ERROR,
                            message=(
                                f'Could not resolve subpipeline input "{port_name}" '
                                f'on "{name}".'
                            ),
                            path=("pipeline", name, port_name),
                        )
                    )

    diagnostics.extend(_detect_cycles(graph))
    return diagnostics


def _detect_cycles(graph: LogicalGraph) -> list[Diagnostic]:
    """Detect directed cycles using DFS."""
    adjacency: dict[str, list[str]] = {n.name: [] for n in graph.nodes}
    for edge in graph.edges:
        adjacency.setdefault(edge.producer_node, []).append(edge.consumer_node)

    WHITE, GRAY, BLACK = 0, 1, 2
    color = {name: WHITE for name in adjacency}
    diagnostics: list[Diagnostic] = []
    stack: list[str] = []

    def visit(node: str) -> None:
        color[node] = GRAY
        stack.append(node)
        for nxt in adjacency.get(node, []):
            if color.get(nxt, WHITE) == GRAY:
                cycle_start = stack.index(nxt)
                cycle = [*stack[cycle_start:], nxt]
                diagnostics.append(
                    Diagnostic(
                        code="PMPIPE301",
                        severity=Severity.ERROR,
                        message=f"Pipeline contains a cycle: {' -> '.join(cycle)}.",
                        path=("pipeline",),
                        metadata={"cycle": cycle},
                    )
                )
            elif color.get(nxt, WHITE) == WHITE:
                visit(nxt)
        stack.pop()
        color[node] = BLACK

    for name in adjacency:
        if color[name] == WHITE:
            visit(name)

    return diagnostics


def _validate_port_compatibility(
    graph: LogicalGraph, pipeline_cls: type[Pipeline]
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    nodes = graph.node_map()

    for edge in graph.edges:
        producer = nodes.get(edge.producer_node)
        consumer = nodes.get(edge.consumer_node)
        if producer is None or consumer is None:
            continue

        producer_port = next(
            (p for p in producer.outputs if p.name == edge.producer_port), None
        )
        consumer_port = next(
            (p for p in consumer.inputs if p.name == edge.consumer_port), None
        )
        if producer_port is None:
            diagnostics.append(
                Diagnostic(
                    code="PMPIPE201",
                    severity=Severity.ERROR,
                    message=(
                        f'Unknown producer port "{edge.producer_port}" on '
                        f'"{edge.producer_node}" wired to '
                        f'"{edge.consumer_node}.{edge.consumer_port}".'
                    ),
                    path=("pipeline", edge.consumer_node, edge.consumer_port),
                    related=(("pipeline", edge.producer_node, edge.producer_port),),
                )
            )
            continue
        if consumer_port is None:
            diagnostics.append(
                Diagnostic(
                    code="PMPIPE201",
                    severity=Severity.ERROR,
                    message=(
                        f'Unknown consumer port "{edge.consumer_port}" on '
                        f'"{edge.consumer_node}".'
                    ),
                    path=("pipeline", edge.consumer_node, edge.consumer_port),
                )
            )
            continue

        prod_type = producer_port.contract_type
        cons_type = consumer_port.contract_type
        if prod_type is None or cons_type is None:
            continue

        if not _contracts_compatible(prod_type, cons_type):
            diagnostics.append(
                Diagnostic(
                    code="PMPIPE210",
                    severity=Severity.ERROR,
                    message=(
                        f'The step "{edge.consumer_node}" expects '
                        f"{getattr(cons_type, '__name__', cons_type)} on "
                        f'"{edge.consumer_port}", but received '
                        f"{getattr(prod_type, '__name__', prod_type)} from "
                        f'"{edge.producer_node}.{edge.producer_port}".'
                    ),
                    path=("pipeline", edge.consumer_node, edge.consumer_port),
                    related=(("pipeline", edge.producer_node, edge.producer_port),),
                    help=(
                        "Connect a compatible output or change the consumer contract."
                    ),
                    metadata={
                        "producer_contract": contract_id(prod_type),
                        "consumer_contract": contract_id(cons_type),
                        "producer_published_id": published_contract_id(prod_type),
                        "consumer_published_id": published_contract_id(cons_type),
                    },
                )
            )

    return diagnostics


def _contracts_compatible(producer: type[Any], consumer: type[Any]) -> bool:
    """Return True when producer/consumer contracts are the same logical type.

    Exact Python identity remains the primary check. Distinct classes that share
    the same published ODCS/CCM identity (common after ODCS load) are also
    treated as compatible.
    """
    if producer is consumer:
        return True
    left = published_contract_id(producer)
    right = published_contract_id(consumer)
    return bool(left and right and left == right)


def validate_transformation(transform: type[Transformation]) -> ValidationReport:
    """Validate a transformation class definition in isolation."""
    diagnostics: list[Diagnostic] = []
    for problem in transform.validate_definition():
        diagnostics.append(
            Diagnostic(
                code="PMTRN001",
                severity=Severity.ERROR,
                message=problem,
                path=("transformation", transform.__name__),
            )
        )
    for port in list(transform.inputs()) + list(transform.outputs()):
        if port.contract_type is not None and not is_data_contract_type(
            port.contract_type
        ):
            diagnostics.append(
                Diagnostic(
                    code="PMDATA101",
                    severity=Severity.ERROR,
                    message=(
                        f'Port "{port.name}" does not reference a ContractModel type.'
                    ),
                    path=("transformation", transform.__name__, port.name),
                )
            )
    return ValidationReport.from_diagnostics(diagnostics)
