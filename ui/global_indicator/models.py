from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

from dash.development.base_component import Component


@dataclass(frozen=True, slots=True)
class IndicatorData:
    real_value: str | Component
    color_value: str | Component
    temporality: str | None = None
    plan_value: str | Component | None = None
    only_last_measurement: bool = False


@dataclass(frozen=True, slots=True)
class GlobalIndicatorData:
    label: str
    unit: str
    indicators: tuple[IndicatorData, ...]

    @classmethod
    def from_iterable(cls, label: str, unit: str, indicators: tuple[IndicatorData, ...]) -> GlobalIndicatorData:
        return cls(label=label, unit=unit, indicators=tuple(indicators))

    def to_component(self) -> Component:
        from .build import build_global_indicator
        return build_global_indicator(model=self)


@dataclass(frozen=True, slots=True)
class GlobalIndicatorsData:
    components: tuple[GlobalIndicatorData, ...]

    @classmethod
    def from_iterable(cls, components: tuple[GlobalIndicatorData, ...]) -> GlobalIndicatorsData:
        return cls(components=tuple(components))

    def to_component(self) -> Component:
        from .build import build_global_indicators
        return build_global_indicators(model=self)

    def __iter__(self) -> Iterator[GlobalIndicatorData]:
        return iter(self.components)

    def __len__(self) -> int:
        return len(self.components)
