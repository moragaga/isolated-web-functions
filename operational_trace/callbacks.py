from __future__ import annotations

from dash import ALL, ClientsideFunction, Input, Output, State

from .ids import OperationalTraceIds


def register_operational_trace_callbacks(
    *,
    app,
    scope_id: str,
) -> None:
    selector_pattern = OperationalTraceIds.alarm_selector_pattern(
        scope_id=scope_id,
        alarm=ALL,
    )
    route_pattern = OperationalTraceIds.route_pattern(
        scope_id=scope_id,
        alarm=ALL,
    )
    marker_pattern = OperationalTraceIds.marker_pattern(
        scope_id=scope_id,
        alarm=ALL,
        process=ALL,
    )

    app.clientside_callback(
        ClientsideFunction(
            namespace='operational_trace',
            function_name='update_selection',
        ),
        Output(OperationalTraceIds.selection_store(scope_id), 'data'),
        Input(selector_pattern, 'n_clicks_timestamp'),
        Input(OperationalTraceIds.snapshot_store(scope_id), 'data'),
        State(selector_pattern, 'id'),
        State(OperationalTraceIds.selection_store(scope_id), 'data'),
        prevent_initial_call=False,
    )

    app.clientside_callback(
        ClientsideFunction(
            namespace='operational_trace',
            function_name='render_selection',
        ),
        Output(OperationalTraceIds.root(scope_id), 'data-selected-alarm-id'),
        Output(OperationalTraceIds.root(scope_id), 'data-has-selection'),
        Output(selector_pattern, 'data-selected'),
        Output(selector_pattern, 'aria-pressed'),
        Output(route_pattern, 'data-selected'),
        Output(marker_pattern, 'data-selected'),
        Input(OperationalTraceIds.selection_store(scope_id), 'data'),
        Input(OperationalTraceIds.snapshot_store(scope_id), 'data'),
        State(selector_pattern, 'id'),
        State(route_pattern, 'id'),
        State(marker_pattern, 'id'),
    )
