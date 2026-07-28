from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

class LabelPosition(StrEnum):
    TOP = 'top'
    BOTTOM = 'bottom'
    LEFT = 'left'
    RIGHT = 'right'

class ImagesOrientation(StrEnum):
    VERTICAL = 'vertical'
    HORIZONTAL = 'horizontal'

@dataclass(frozen=True, slots=True)
class OverrideState:
    override: bool = False
    state: str | None = None

@dataclass(frozen=True, slots=True)
class WrappedImageDefinition:
    label: str | None = None
    label_font_size: str | None  = None
    label_position: LabelPosition = LabelPosition.TOP
    image: str | None = None
    state_kpi_key: str | None = None
    override_state: OverrideState  = OverrideState()

    def __post_init__(self):
        object.__setattr__(self, 'label_font_size', self._safe_text(self.label_font_size))
        object.__setattr__(self, 'image', self._safe_text(self.image))
        object.__setattr__(self, 'state_kpi_key', self._safe_text(self.state_kpi_key))

    @staticmethod
    def _safe_text(value: str) -> str:
        return (value or '').lower()

@dataclass(frozen=True, slots=True)
class WrappedImageGroupDefinition:
    images_orientation: ImagesOrientation = ImagesOrientation.VERTICAL
    images: tuple[WrappedImageDefinition, ...] = tuple()
