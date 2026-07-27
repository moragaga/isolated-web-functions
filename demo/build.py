from __future__ import annotations

from dash import dcc, html
from dash.development.base_component import Component

from operational_trace import OperationalTraceDefinition
from operational_trace.build import build_operational_trace_module

from .data import (
    build_distributed_definition,
    build_integrated_definition,
    build_process_definition,
    resolve_distributed_active_selection_key,
)
from .ids import DemoIds


def build_demo_layout() -> Component:
    return html.Main(
        className='operational-trace-demo',
        children=[
            dcc.Interval(
                id=DemoIds.INTERVAL,
                interval=5_000,
                n_intervals=0,
            ),
            html.Header(
                className='operational-trace-demo__header',
                children=[
                    html.H1(children=['Operational trace · iteration 4']),
                    html.P(
                        children=[
                            'Consulta cada 5 segundos y cambio de ocurrencia en la cuarta revisión.'
                        ],
                    ),
                ],
            ),
            _build_demo_section(
                title='Proceso normal',
                description='Seis posiciones visuales y una traza operacional central.',
                definition=build_process_definition(revision=0),
            ),
            _build_demo_section(
                title='Proceso distribuido',
                description=(
                    'Las distribuidas comparten el último espacio cuando superan el umbral.'
                ),
                definition=build_distributed_definition(revision=0),
                active_distributed_selection_key=(
                    resolve_distributed_active_selection_key(
                        n_intervals=0,
                        revision=0,
                    )
                ),
            ),
            _build_demo_section(
                title='Operaciones Integradas',
                description=(
                    'Las alarmas mantienen el ancho de un proceso y un máximo de tres por grupo.'
                ),
                definition=build_integrated_definition(revision=0),
            ),
        ],
    )


def _build_demo_section(
    *,
    title: str,
    description: str,
    definition: OperationalTraceDefinition,
    active_distributed_selection_key: str | None = None,
) -> Component:
    return html.Section(
        className='operational-trace-demo__section',
        children=[
            html.Div(
                className='operational-trace-demo__section-header',
                children=[
                    html.Div(
                        children=[
                            html.H2(children=[title]),
                            html.P(children=[description]),
                        ],
                    ),
                    html.Output(
                        id=DemoIds.status(definition.scope_id),
                        className='operational-trace-demo__status',
                        children=['Snapshot 0 · consulta 0'],
                    ),
                ],
            ),
            build_operational_trace_module(
                definition=definition,
                snapshot_version='0',
                active_distributed_selection_key=(
                    active_distributed_selection_key
                ),
            ),
            html.Div(
                className=(
                    'operational-trace-demo__process-grid '
                    f'operational-trace-demo__process-grid--{definition.mode.value}'
                ),
                style={
                    'gridTemplateColumns': (
                        f'repeat({len(definition.points)}, minmax(0, 1fr))'
                    ),
                },
                children=[
                    html.Div(
                        className='operational-trace-demo__process-card',
                        children=[point.label],
                    )
                    for point in definition.points
                ],
            ),
        ],
    )
