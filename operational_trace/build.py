from __future__ import annotations

from dash import dcc, html
from dash.development.base_component import Component

from .enums import OperationalTraceMode
from .geometry import resolve_alarm_route_geometry, resolve_process_positions
from .ids import OperationalTraceIds
from .models import AlarmDefinition, OperationalTraceDefinition
from .placement import resolve_alarm_placements
from .serialization import serialize_snapshot


def build_operational_trace_module(
    *,
    definition: OperationalTraceDefinition,
    snapshot_version: str = '0',
    active_distributed_selection_key: str | None = None,
) -> Component:
    return html.Section(
        id=OperationalTraceIds.module(definition.scope_id),
        className=(
            'operational-trace-module '
            f'operational-trace-module--{definition.mode.value}'
        ),
        **{
            'data-operational-trace-scope': definition.scope_id,
        },
        children=[
            dcc.Store(
                id=OperationalTraceIds.snapshot_store(definition.scope_id),
                storage_type='memory',
                data=serialize_snapshot(
                    definition=definition,
                    version=snapshot_version,
                ),
            ),
            dcc.Store(
                id=OperationalTraceIds.selection_store(definition.scope_id),
                storage_type='memory',
                data={
                    'selection_key': None,
                    'last_event_timestamp': -1,
                },
            ),
            build_alarm_board(
                definition=definition,
                active_distributed_selection_key=active_distributed_selection_key,
            ),
            build_operational_trace(definition=definition),
        ],
    )


def build_alarm_board(
    *,
    definition: OperationalTraceDefinition,
    active_distributed_selection_key: str | None = None,
) -> Component:
    if definition.mode is OperationalTraceMode.INTEGRATED_OPERATIONS:
        return _build_integrated_alarm_board(definition=definition)
    if definition.mode is OperationalTraceMode.DISTRIBUTED:
        return _build_distributed_alarm_board(
            definition=definition,
            active_distributed_selection_key=active_distributed_selection_key,
        )
    return _build_process_alarm_board(definition=definition)


def build_operational_trace(
    *,
    definition: OperationalTraceDefinition,
) -> Component:
    return html.Div(
        id=OperationalTraceIds.root(definition.scope_id),
        className=(
            'operational-trace '
            f'operational-trace--{definition.mode.value}'
        ),
        **{
            'data-selected-alarm-id': '',
            'data-has-selection': 'false',
        },
        children=[
            html.Div(
                id=OperationalTraceIds.route_layer(definition.scope_id),
                className='operational-trace__alarm-layer',
                children=build_alarm_routes(definition=definition),
            ),
            html.Div(className='operational-trace__baseline'),
            html.Div(
                id=OperationalTraceIds.point_layer(definition.scope_id),
                className='operational-trace__points',
                children=build_operational_points(definition=definition),
            ),
        ],
    )


def build_alarm_routes(
    *,
    definition: OperationalTraceDefinition,
) -> list[Component]:
    placements = resolve_alarm_placements(definition=definition)
    return [
        _build_alarm_route(
            definition=definition,
            alarm=alarm,
            placement=placements[alarm.selection_key],
        )
        for alarm in definition.ordered_alarms
    ]


def build_operational_points(
    *,
    definition: OperationalTraceDefinition,
) -> list[Component]:
    process_positions = resolve_process_positions(definition=definition)
    return [
        html.Div(
            className='operational-trace__point',
            title=point.label,
            style={
                '--operational-trace-point-x': (
                    f'{process_positions[point.key]:.6f}%'
                ),
            },
            **{
                'data-process-key': point.key,
            },
            children=[
                html.Span(className='operational-trace__point-core'),
                *_build_point_markers(
                    definition=definition,
                    process_key=point.key,
                ),
            ],
        )
        for point in definition.points
    ]


def _build_process_alarm_board(
    *,
    definition: OperationalTraceDefinition,
) -> Component:
    return html.Div(
        id=OperationalTraceIds.board(definition.scope_id),
        className='operational-alarm-board operational-alarm-board--process',
        style={
            '--operational-alarm-slot-count': str(definition.process_slot_count),
        },
        children=[
            _build_alarm_card(
                alarm=alarm,
                scope_id=definition.scope_id,
                grid_column=index + 1,
            )
            for index, alarm in enumerate(definition.ordered_alarms)
        ],
    )


def _build_distributed_alarm_board(
    *,
    definition: OperationalTraceDefinition,
    active_distributed_selection_key: str | None,
) -> Component:
    distributed_alarms = tuple(
        alarm
        for alarm in definition.ordered_alarms
        if alarm.is_distributed
    )
    if len(distributed_alarms) <= definition.distributed_threshold:
        return html.Div(
            id=OperationalTraceIds.board(definition.scope_id),
            className=(
                'operational-alarm-board '
                'operational-alarm-board--distributed-flat'
            ),
            style={
                '--operational-alarm-slot-count': str(
                    definition.process_slot_count
                ),
            },
            children=[
                _build_alarm_card(
                    alarm=alarm,
                    scope_id=definition.scope_id,
                    grid_column=index + 1,
                )
                for index, alarm in enumerate(definition.ordered_alarms)
            ],
        )

    normal_alarms = tuple(
        alarm
        for alarm in definition.ordered_alarms
        if not alarm.is_distributed
    )
    active_selection_key = _resolve_active_distributed_selection_key(
        alarms=distributed_alarms,
        active_selection_key=active_distributed_selection_key,
    )

    return html.Div(
        id=OperationalTraceIds.board(definition.scope_id),
        className=(
            'operational-alarm-board '
            'operational-alarm-board--distributed-isolated'
        ),
        style={
            '--operational-alarm-slot-count': str(definition.process_slot_count),
        },
        children=[
            *[
                _build_alarm_card(
                    alarm=alarm,
                    scope_id=definition.scope_id,
                    grid_column=index + 1,
                )
                for index, alarm in enumerate(normal_alarms)
            ],
            html.Div(
                className='operational-alarm-board__rotator',
                style={'gridColumn': str(definition.process_slot_count)},
                **{
                    'data-active-alarm-id': active_selection_key,
                    'data-rotation-count': str(len(distributed_alarms)),
                },
                children=[
                    _build_alarm_card(
                        alarm=alarm,
                        scope_id=definition.scope_id,
                        rotation_active=(
                            alarm.selection_key == active_selection_key
                        ),
                    )
                    for alarm in distributed_alarms
                ],
            ),
        ],
    )


def _build_integrated_alarm_board(
    *,
    definition: OperationalTraceDefinition,
) -> Component:
    placements = resolve_alarm_placements(definition=definition)
    return html.Div(
        id=OperationalTraceIds.board(definition.scope_id),
        className=(
            'operational-alarm-board '
            'operational-alarm-board--integrated'
        ),
        style={
            '--operational-alarm-slot-count': str(len(definition.points)),
        },
        children=[
            _build_alarm_card(
                alarm=alarm,
                scope_id=definition.scope_id,
                grid_column=placements[alarm.selection_key].slot_index + 1,
            )
            for alarm in definition.ordered_alarms
        ],
    )


def _build_alarm_card(
    *,
    alarm: AlarmDefinition,
    scope_id: str,
    grid_column: int | None = None,
    rotation_active: bool = True,
) -> Component:
    style = None if grid_column is None else {'gridColumn': str(grid_column)}
    return html.Article(
        className=(
            'operational-alarm-card '
            f'operational-alarm-card--{alarm.tone.value}'
        ),
        style=style,
        **{
            'data-rotation-active': str(rotation_active).lower(),
            'data-alarm-id': alarm.alarm_id,
            'data-alarm-occurrence-id': alarm.selection_key,
        },
        children=[
            html.Div(
                id=OperationalTraceIds.alarm_selector(
                    scope_id=scope_id,
                    selection_key=alarm.selection_key,
                ),
                className='operational-alarm-card__selector',
                role='button',
                tabIndex=0,
                n_clicks=0,
                n_clicks_timestamp=-1,
                **{
                    'aria-pressed': 'false',
                    'data-selected': 'false',
                },
                children=[
                    html.Span(
                        className='operational-alarm-card__criticality',
                        children=[alarm.criticality],
                    ),
                    html.Span(
                        className='operational-alarm-card__title',
                        title=alarm.title,
                        children=[alarm.title],
                    ),
                    html.Span(
                        className='operational-alarm-card__time',
                        children=[alarm.active_time],
                    ),
                ],
            ),
            html.Button(
                className='operational-alarm-card__action',
                type='button',
                children=['Gestionar'],
            ),
        ],
    )


def _build_alarm_route(
    *,
    definition: OperationalTraceDefinition,
    alarm: AlarmDefinition,
    placement,
) -> Component:
    geometry = resolve_alarm_route_geometry(
        definition=definition,
        alarm=alarm,
        placement=placement,
    )
    children: list[Component] = []

    if geometry.has_horizontal_trunk:
        children.extend(
            [
                html.Span(
                    className='operational-trace__route-card-connector',
                    style={
                        '--operational-trace-line-x': (
                            f'{geometry.card_x_percent:.6f}%'
                        ),
                    },
                ),
                html.Span(
                    className='operational-trace__route-trunk',
                    style={
                        '--operational-trace-line-start': (
                            f'{geometry.trunk_start_x_percent:.6f}%'
                        ),
                        '--operational-trace-line-end': (
                            f'{geometry.trunk_end_x_percent:.6f}%'
                        ),
                    },
                ),
                *[
                    html.Span(
                        className=(
                            'operational-trace__route-process-connector'
                        ),
                        style={
                            '--operational-trace-line-x': f'{position:.6f}%',
                        },
                    )
                    for position in geometry.process_x_percents
                ],
            ]
        )
    else:
        children.append(
            html.Span(
                className='operational-trace__route-local-connector',
                style={
                    '--operational-trace-line-x': (
                        f'{geometry.origin_x_percent:.6f}%'
                    ),
                },
            )
        )

    return html.Div(
        id=OperationalTraceIds.route(
            scope_id=definition.scope_id,
            selection_key=alarm.selection_key,
        ),
        className=(
            'operational-trace__route '
            f'operational-trace__route--{alarm.tone.value}'
        ),
        **{
            'data-selected': 'false',
            'data-alarm-id': alarm.alarm_id,
            'data-alarm-occurrence-id': alarm.selection_key,
        },
        children=children,
    )


def _build_point_markers(
    *,
    definition: OperationalTraceDefinition,
    process_key: str,
) -> list[Component]:
    markers: list[Component] = []
    for alarm in definition.ordered_alarms:
        marker_type = _resolve_marker_type(
            alarm=alarm,
            process_key=process_key,
        )
        if marker_type is None:
            continue
        markers.append(
            html.Span(
                id=OperationalTraceIds.marker(
                    scope_id=definition.scope_id,
                    selection_key=alarm.selection_key,
                    process_key=process_key,
                ),
                className=(
                    'operational-trace__marker '
                    f'operational-trace__marker--{marker_type} '
                    f'operational-trace__marker--{alarm.tone.value}'
                ),
                **{
                    'data-selected': 'false',
                },
                children=_build_marker_icons(marker_type=marker_type),
            )
        )
    return markers


def _resolve_marker_type(
    *,
    alarm: AlarmDefinition,
    process_key: str,
) -> str | None:
    if alarm.is_local_route and process_key == alarm.origin_process_key:
        return 'contract'
    if process_key == alarm.origin_process_key:
        return 'up'
    if process_key in alarm.affected_process_keys:
        return 'down'
    return None


def _build_marker_icons(*, marker_type: str) -> list[Component]:
    directions = ('up', 'down') if marker_type == 'contract' else (marker_type,)
    return [
        html.Span(
            className=(
                'operational-trace__marker-icon '
                f'operational-trace__marker-icon--{direction}'
            ),
            children=[
                html.I(className=f'bi bi-chevron-{direction}'),
            ],
        )
        for direction in directions
    ]


def _resolve_active_distributed_selection_key(
    *,
    alarms: tuple[AlarmDefinition, ...],
    active_selection_key: str | None,
) -> str:
    available_keys = {alarm.selection_key for alarm in alarms}
    if active_selection_key in available_keys:
        return active_selection_key
    return alarms[0].selection_key
