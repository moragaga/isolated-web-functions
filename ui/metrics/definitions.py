from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

DisplayOptionalDefinition: TypeAlias = str | None

@dataclass(frozen=True, slots=True)
class StandardMetricRowDefinition:
    label: str

    value_key: DisplayOptionalDefinition = None
    value_color_key: DisplayOptionalDefinition = None
    unit: DisplayOptionalDefinition = None

    container_class_name: DisplayOptionalDefinition = None
    font_size_class_name: DisplayOptionalDefinition = None


@dataclass(frozen=True, slots=True)
class DualMetricRowDefinition:
    initial_label: str

    first_label: DisplayOptionalDefinition = None
    first_value_key: DisplayOptionalDefinition = None
    first_value_color_key: DisplayOptionalDefinition = None
    first_unit: DisplayOptionalDefinition = None

    divider_value: DisplayOptionalDefinition = None

    second_label: DisplayOptionalDefinition = None
    second_value_key: DisplayOptionalDefinition = None
    second_value_color_key: DisplayOptionalDefinition = None
    second_unit: DisplayOptionalDefinition = None

    divider_class_name: DisplayOptionalDefinition = None
    container_class_name: DisplayOptionalDefinition = None
    font_size_class_name: DisplayOptionalDefinition = None
