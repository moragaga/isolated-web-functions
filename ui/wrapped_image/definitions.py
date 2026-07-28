from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Literal


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
        object.__setattr__(self, 'label', self._normalize_text(value=self.label, formatted='normal'))
        object.__setattr__(self, 'label_font_size', self._normalize_text(value=self.label_font_size))
        object.__setattr__(self, 'image', self._normalize_text(value=self.image))
        object.__setattr__(self, 'state_kpi_key', self._normalize_text(value=self.state_kpi_key))

    @staticmethod
    def _normalize_text(
        *,
        value: str,
        formatted: Literal['upper', 'lower', 'capitalized', 'normal'] = 'lower'
    ) -> str:
        value = value or ''
        match formatted:
            case 'upper':
                return value.upper()
            case 'lower':
                return value.lower()
            case 'capitalized':
                return value.capitalize()
            case 'normal':
                return value

@dataclass(frozen=True, slots=True)
class WrappedImageGroupDefinition:
    images_orientation: ImagesOrientation = ImagesOrientation.VERTICAL
    images: tuple[WrappedImageDefinition, ...] = tuple()
