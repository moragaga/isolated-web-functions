from __future__ import annotations

from typing import Any
from .definitions import WrappedImageDefinition, WrappedImageGroupDefinition
from .models import WrappedImageModel, WrappedImageGroupModel

def map_image(
    *,
    definition: WrappedImageDefinition,
    kpis: dict[str, Any],
) -> WrappedImageModel:
    return WrappedImageModel(
        label=definition.label,
        label_font_size=definition.label_font_size,
        label_position=definition.label_position,
        image=definition.image,
        variant=kpis.get(definition.state_kpi_key),
        override_state=definition.override_state,
    )

def map_image_group(
    *,
    definitions: WrappedImageGroupDefinition,
    kpis: dict[str, Any],
) -> WrappedImageGroupModel:
    return WrappedImageGroupModel.from_iterable(
        images_orientation=definitions.images_orientation,
        images=(
            map_image(definition=definition, kpis=kpis)
            for definition in definitions.images
        )
    )