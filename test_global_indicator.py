from ui.global_indicator.definitions import IndicatorDefinition, GlobalIndicatorDefinition, \
    IndicatorPropertiesDefinition
from ui.global_indicator.mappers import map_global_indicators_data


_PROPERTIES: IndicatorPropertiesDefinition = IndicatorPropertiesDefinition(
    label='font-size-gi-300',
    temporality='font-size-gi-200',
    real_value='font-size-gi-100',
    plan_value='font-size-gi-200',
    last_measurement_label='font-size-gi-400',
    last_measurement_value='font-size-gi-300'
)

DEFINITIONS: tuple[GlobalIndicatorDefinition, ...] = (
    GlobalIndicatorDefinition(
        label='TEST_1',
        unit='%',
        properties=_PROPERTIES,
        indicators=(
            IndicatorDefinition(
                temporality='Día',
                indicator_key='test',
            ),
            IndicatorDefinition(
                temporality='Semana',
                indicator_key='test',
            ),
        )
    ),
    GlobalIndicatorDefinition(
        label='TEST_2TEST_2TEST_2TEST_2TEST_2TEST_2TEST_2TEST_2TEST_2',
        unit='%',
        properties=_PROPERTIES,
        indicators=(
            IndicatorDefinition(
                temporality='Día',
                indicator_key='test',
            ),
            IndicatorDefinition(
                temporality='Semana',
                indicator_key='test',
            ),
        )
    ),
    GlobalIndicatorDefinition(
        label='TEST_3',
        unit='%',
        properties=_PROPERTIES,
        indicators=(
            IndicatorDefinition(
                temporality='Día',
                indicator_key='test',
            ),
            IndicatorDefinition(
                temporality='Semana',
                indicator_key='test',
            ),
        )
    ),
    GlobalIndicatorDefinition(
        label='TEST_4',
        unit='%',
        properties=_PROPERTIES,
        indicators=(
            IndicatorDefinition(
                temporality='Día',
                indicator_key='test',
            ),
            IndicatorDefinition(
                temporality='Semana',
                indicator_key='test',
            ),
            IndicatorDefinition(
                temporality='actual',
                indicator_key='test',
                only_last_measurement=True,
            )
        )
    ),
    GlobalIndicatorDefinition(
        label='TEST_5',
        unit='%',
        properties=_PROPERTIES,
        indicators=(
            IndicatorDefinition(
                temporality='Día',
                indicator_key='test',
            ),
            IndicatorDefinition(
                temporality='Semana',
                indicator_key='test',
            ),
            IndicatorDefinition(
                temporality='actual',
                indicator_key='test',
                only_last_measurement=True,
            )
        )
    )
)

kpis = {
    '': 'X',
    'test_dia_real_inst': '1000000',
    'test_semana_real_inst': '20000000',
    'test_dia_plan_inst': '100,30',
    'test_semana_plan_inst': '250',
    'test_actual_real_inst': '20'
}

global_indicators = map_global_indicators_data(
    definitions=DEFINITIONS,
    kpis=kpis,
)

component = global_indicators.to_component()

