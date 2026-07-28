from __future__ import annotations

from ui.wrapped_image.definitions import (
    WrappedImageDefinition,
    WrappedImageGroupDefinition,
    LabelPosition,
    OverrideState,
    ImagesOrientation
)
from ui.wrapped_image.mappers import map_image, map_image_group


DEFINITION_CH1 = WrappedImageDefinition(
    label='CH-1',
    label_font_size='font-size-100',
    label_position=LabelPosition.RIGHT,
    image='chancador',
    state_kpi_key='chancador_1_estado_inst',
)
DEFINITION_CH2 = WrappedImageDefinition(
    label='CH-2',
    label_font_size='font-size-100',
    label_position=LabelPosition.BOTTOM,
    image='chancador',
    state_kpi_key='chancador_2_estado_inst',
    override_state=OverrideState(
        override=True,
        state='operando'
    )
)

DEFINITIONS = WrappedImageGroupDefinition(
    images_orientation=ImagesOrientation.HORIZONTAL,
    images=(
        DEFINITION_CH1,
        DEFINITION_CH2,
    )
)
kpis = {'chancador_1_estado_inst': 'operando', 'chancador_2_estado_inst': 'operando'}
ch1 = map_image(definition=DEFINITION_CH1, kpis=kpis).to_component()
chs = map_image_group(definitions=DEFINITIONS, kpis=kpis).to_component()