from __future__ import annotations

from dash import html

from ui.metrics.definitions import StandardMetricRowDefinition, DualMetricRowDefinition
from ui.metrics.mappers import map_standard_metrics_rows, map_dual_metrics_rows


STANDARD_DEFINITION: tuple[StandardMetricRowDefinition, ...] = (
    StandardMetricRowDefinition(
        label='TEST_1',
        value_key='test_1_value_key',
        value_color_key='test_1_color_key',
        unit='%',
        font_size_class_name='fs-6'
    ),
    StandardMetricRowDefinition(
        label='TEST_2',
        value_key='test_2_value_key',
        value_color_key='test_2_color_key',
        unit='%',
        font_size_class_name='fs-6'
    ),
)

DUAL_DEFINITION: tuple[DualMetricRowDefinition, ...] = (
    DualMetricRowDefinition(
        initial_label='TEST',
        first_label='TEST_1',
        first_value_key='test_1_value_key',
        first_value_color_key='test_1_color_key',
        first_unit='%',
        second_label='TEST_2',
        second_value_key='test_2_value_key',
        second_value_color_key='test_2_color_key',
        second_unit='%',
        divider_value='/',
        font_size_class_name='fs-6'
    ),
)

kpis = {'': 'X', 'test_1_value_key': '10', 'test_2_value_key': '20'}

standard = map_standard_metrics_rows(definitions=STANDARD_DEFINITION, kpis=kpis)
dual = map_dual_metrics_rows(definitions=DUAL_DEFINITION, kpis=kpis)


component = html.Div(
    className='',
    children=[
        html.Div(
            className='d-flex w-100 flex-column',
            children=standard.to_components()
        ),
        html.Div(
            className='d-flex w-100 flex-column',
            children=dual.to_components()
        )
    ]
)