from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias, Iterable, Iterator

from dash.development.base_component import Component

DisplayValue: TypeAlias = str | int | float | Component | None
DisplayOptionalValue: TypeAlias = str | None


@dataclass(frozen=True, slots=True)
class StandardMetricRowData:
    label: str

    value: DisplayValue = None
    value_color: DisplayValue = None
    unit: DisplayOptionalValue = None

    container_class_name: DisplayOptionalValue = None
    font_size_class_name: DisplayOptionalValue = None

    def to_component(self) -> Component:
        from .build import build_inline_metric_row
        return build_inline_metric_row(model=self)

@dataclass(frozen=True, slots=True)
class DualMetricRowData:
    initial_label: str

    first_label: DisplayOptionalValue = None
    first_value: DisplayValue = None
    first_value_color: DisplayValue = None
    first_unit: DisplayOptionalValue = None

    divider_value: DisplayOptionalValue = None

    second_label: DisplayOptionalValue = None
    second_value: DisplayValue = None
    second_value_color: DisplayValue = None
    second_unit: DisplayOptionalValue = None

    divider_class_name: DisplayOptionalValue = None
    container_class_name: DisplayOptionalValue = None
    font_size_class_name: DisplayOptionalValue = None

    def to_component(self) -> Component:
        from .build import build_inline_dual_metric_row
        return build_inline_dual_metric_row(model=self)

MetricRowData: TypeAlias = StandardMetricRowData | DualMetricRowData

@dataclass(frozen=True, slots=True)
class MetricsRowsData:
    metrics: tuple[MetricRowData, ...]

    @classmethod
    def from_iterable(cls, metrics: Iterable[MetricRowData]) -> MetricsRowsData:
        return cls(metrics=tuple(metrics))

    def to_components(self) -> list[Component]:
        return [metric.to_component() for metric in self.metrics]

    def __iter__(self) -> Iterator[MetricRowData]:
        return iter(self.metrics)

    def __len__(self) -> int:
        return len(self.metrics)
