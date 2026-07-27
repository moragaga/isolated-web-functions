from __future__ import annotations

from dash import html
from dash.development.base_component import Component

from .models import IndicatorData


def build_label(
    *,
    label: str,
    unit: str,
) -> Component:
    return html.Div(
        className='global-indicator__heading',
        children=[
            html.P(
                className='global-indicator__label',
                title=label,
                children=[label],
            ),
            html.I(
                className='global-indicator__icon bi bi-arrow-right-short px-1',
            ),
            html.P(
                className='global-indicator__unit',
                children=[unit],
            ),
        ],
    )


def build_indicator_content(
    *,
    indicators: tuple[IndicatorData, ...],
) -> tuple[Component, Component | None]:
    last_measurement_component = None
    table_rows = []

    for indicator in indicators:
        if indicator.only_last_measurement:
            last_measurement_component = _build_last_measurement(
                value=indicator.real_value,
                color=indicator.color_value,
            )
            continue

        table_rows.append(_build_table_row(model=indicator))

    return _build_table(rows=table_rows), last_measurement_component


def _build_table(
    *,
    rows: list[Component],
) -> Component:
    return html.Table(
        className='global-indicator__table',
        children=[
            html.Tbody(children=rows),
        ],
    )


def _build_table_row(
    *,
    model: IndicatorData,
) -> Component:
    return html.Tr(
        className='global-indicator__row',
        children=[
            _build_table_value_cell(
                value=model.temporality,
                value_class_name='global-indicator__value--temporality',
                is_header=True,
            ),
            _build_table_value_cell(
                value=model.real_value,
                color=model.color_value,
                value_class_name='global-indicator__value--real',
            ),
            _build_table_separator_cell(),
            _build_table_value_cell(
                value=model.plan_value,
                value_class_name='global-indicator__value--plan',
            ),
        ],
    )


def _build_table_value_cell(
    *,
    value: str | Component,
    color: str | Component | None = None,
    value_class_name: str = '',
    is_header: bool = False,
) -> Component:
    component = html.Th if is_header else html.Td
    properties = {'scope': 'row'} if is_header else {}

    return component(
        className='global-indicator__cell',
        children=[
            html.P(
                className='{0} {1} {2}'.format(
                    'global-indicator__value',
                    value_class_name,
                    _safe_color(color=color),
                ),
                children=[_safe_value(value=value)],
            ),
        ],
        **properties,
    )


def _build_table_separator_cell() -> Component:
    return html.Td(
        className='global-indicator__cell',
        children=[
            html.P(
                className='global-indicator__separator',
                children=['/'],
            ),
        ],
    )


def _build_last_measurement(
    *,
    value: str | Component,
    color: str | Component | None = None,
) -> Component:
    return html.Div(
        className='global-indicator__last-measurement',
        children=[
            html.P(
                className='global-indicator__last-measurement-value {0}'.format(
                    _safe_color(color=color)
                ),
                children=[_safe_value(value=value)],
            ),
            html.P(
                className='global-indicator__last-measurement-label',
                children=['Última medición'],
            ),
        ],
    )


def _safe_value(
    *,
    value: str | Component,
) -> Component:
    if isinstance(value, (str, Component)):
        return value

    return html.Img(
        className='img-fluid',
        src='assets/img/icons/internal/error.svg',
    )


def _safe_color(
    *,
    color: str | Component | None = None,
) -> str:
    if color is None or isinstance(color, Component):
        return ''

    return ''
