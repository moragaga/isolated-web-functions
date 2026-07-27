from __future__ import annotations

from collections.abc import Callable

from dash import Input, Output

from operational_trace import OperationalTraceDefinition
from operational_trace.build import (
    build_alarm_board,
    build_alarm_routes,
    build_operational_points,
)
from operational_trace.ids import OperationalTraceIds
from operational_trace.serialization import serialize_snapshot

from .data import (
    build_distributed_definition,
    build_integrated_definition,
    build_process_definition,
    resolve_demo_revision,
    resolve_distributed_active_selection_key,
)
from .ids import DemoIds


def register_demo_callbacks(*, app) -> None:
    _register_scope_callback(
        app=app,
        scope_id='process-demo',
        definition_builder=build_process_definition,
    )
    _register_scope_callback(
        app=app,
        scope_id='distributed-demo',
        definition_builder=build_distributed_definition,
        active_selection_resolver=resolve_distributed_active_selection_key,
    )
    _register_scope_callback(
        app=app,
        scope_id='integrated-demo',
        definition_builder=build_integrated_definition,
    )


def _register_scope_callback(
    *,
    app,
    scope_id: str,
    definition_builder: Callable[..., OperationalTraceDefinition],
    active_selection_resolver: Callable[..., str] | None = None,
) -> None:
    @app.callback(
        Output(OperationalTraceIds.snapshot_store(scope_id), 'data'),
        Output(OperationalTraceIds.board(scope_id), 'children'),
        Output(OperationalTraceIds.board(scope_id), 'className'),
        Output(OperationalTraceIds.board(scope_id), 'style'),
        Output(OperationalTraceIds.route_layer(scope_id), 'children'),
        Output(OperationalTraceIds.point_layer(scope_id), 'children'),
        Output(DemoIds.status(scope_id), 'children'),
        Input(DemoIds.INTERVAL, 'n_intervals'),
    )
    def update_demo(n_intervals: int):
        revision = resolve_demo_revision(n_intervals=n_intervals)
        definition = definition_builder(revision=revision)
        active_selection_key = (
            active_selection_resolver(
                n_intervals=n_intervals,
                revision=revision,
            )
            if active_selection_resolver is not None
            else None
        )
        board = build_alarm_board(
            definition=definition,
            active_distributed_selection_key=active_selection_key,
        )
        snapshot = serialize_snapshot(
            definition=definition,
            version=str(revision),
        )
        snapshot['poll_sequence'] = n_intervals

        return (
            snapshot,
            board.children,
            board.className,
            board.style,
            build_alarm_routes(definition=definition),
            build_operational_points(definition=definition),
            f'Snapshot {revision} · consulta {n_intervals}',
        )
