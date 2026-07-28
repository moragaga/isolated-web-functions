from __future__ import annotations

from ui.wrapped_image.definitions import (
    WrappedImageDefinition,
    LabelPosition,
)
from ui.wrapped_image.mappers import map_image
from ui.point_card.models import PointCardGroupModel

def _build_definition(index: int) -> WrappedImageDefinition:
    return WrappedImageDefinition(
        label='R{0}'.format(index),
        label_font_size='font-size-100',
        label_position=LabelPosition.TOP,
        image='circle_status',
        state_kpi_key='rougher_{0}_estado_inst'.format(index),
    )

def _build_definitions(total_slots: int) -> tuple[WrappedImageDefinition, ...]:
    return tuple([_build_definition(index=index) for index in range(1, total_slots + 1)])

def _build_point(_kpis: dict):
    return tuple(map_image(definition=definition, kpis=_kpis) for definition in _build_definitions(total_slots=9))

DEFINITIONS: tuple[WrappedImageDefinition, ...] = _build_definitions(total_slots=9)

kpis = {'rougher_{0}_estado_inst'.format(index): ('operando' if index % 2 == 0 else 'detenido') for index in range(1, 9 + 1)}
points = PointCardGroupModel.from_images(images=_build_point(_kpis=kpis)).to_component()

