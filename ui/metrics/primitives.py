from __future__ import annotations

from dash import html
from dash.development.base_component import Component


def build_content(
    *,
    label: str,
    unit: str | None = None,
    value: str | Component,
    color: str | Component,
    is_inside: bool = False,
) -> Component:
    return html.Div(
        className='d-flex w-100',
        children=[
            build_label(label=label, unit=unit, is_inside=is_inside),
            _safe_value(value=value, color=color),
        ]
    )

def build_label(
    *,
    label: str,
    unit: str | None = None,
    is_inside: bool = False,
) -> Component:
    class_name = 'pe-2' if is_inside else ''
    return html.Div(
        className='d-flex w-100 {0}'.format(class_name).strip(),
        children=[
            html.P(className='fw-normal', children=[label]),
            _safe_unit(unit=unit),
        ]
    )

def build_divider(
    *,
    value: str = None,
    class_name: str | None = None,
) -> Component | None:
    if value is None:
        return None

    class_name = class_name or ''
    return html.P(
        className='fw-lighter {0}'.format(class_name).strip(),
        style={'padding': '0 .2rem'},
        children=[value]
    )

def _safe_value(
    *,
    value: str | Component,
    color: str | Component,
) -> Component:
    if isinstance(color, Component):
        color = ''

    # TODO: ADD CALL FUNCTION COLOR CLASSNAME
    return html.P(
        className='fw-bold',
        children=[value]
    )

def _safe_unit(
    *,
    unit: str | None = None,
) -> Component | None:
    if unit is None:
        return None

    def _enclosure(*, value: str):
        return html.P(className='fw-lighter', children=[value])

    return html.Div(
        className='d-flex',
        style={'paddingLeft': '.1rem'},
        children=[
            _enclosure(value='('),
            html.P(className='fw-bold', children=[unit]),
            _enclosure(value=')')
        ]
    )
