from ui.global_indicator.definitions import IndicatorDefinition, GlobalIndicatorDefinition
from ui.global_indicator.mappers import map_global_indicators_data


DEFINITIONS: tuple[GlobalIndicatorDefinition, ...] = (
    GlobalIndicatorDefinition(
        label='TEST_1',
        unit='%',
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

kpis = {'': 'X', 'test_dia_real_inst': '1000000', 'test_semana_real_inst': '20000000'}

global_indicators = map_global_indicators_data(
    definitions=DEFINITIONS,
    kpis=kpis,
)

component = global_indicators.to_component()

