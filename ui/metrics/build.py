from __future__ import annotations

from dash import html
from dash.development.base_component import Component

from .models import StandardMetricRowData, DualMetricRowData
from .primitives import build_label, build_content, build_divider

_GENERIC_ROW_CLASS_NAME = 'd-flex justify-content-between align-items-center w-100 {0} {1}'

def build_inline_metric_row(
    *,
    model: StandardMetricRowData
) -> Component:
    container = model.container_class_name or ''
    font_size = model.font_size_class_name or ''
    return html.Div(
        className=_GENERIC_ROW_CLASS_NAME.format(container, font_size).strip(),
        children=[
            build_content(label=model.label, unit=model.unit, value=model.value, color=model.value_color),
        ]
    )

def build_inline_dual_metric_row(
    *,
    model: DualMetricRowData
) -> Component:
    container = model.container_class_name or ''
    font_size = model.font_size_class_name or ''

    return html.Div(
        className=_GENERIC_ROW_CLASS_NAME.format(container, font_size).strip(),
        children=[
            build_label(label=model.initial_label),
            html.Div(
                className='d-flex',
                children=[
                    build_content(
                        label=model.first_label,
                        unit=model.first_unit,
                        value=model.first_value,
                        color=model.first_value_color,
                        is_inside=True
                    ),
                    build_divider(value=model.divider_value, class_name=model.divider_class_name),
                    build_content(
                        label=model.second_label,
                        unit=model.second_unit,
                        value=model.second_value,
                        color=model.second_value_color,
                        is_inside=True
                    ),
                ]
            )
        ]
    )
