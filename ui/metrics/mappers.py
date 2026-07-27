from __future__ import annotations

from typing import Any

from .definitions import DualMetricRowDefinition, StandardMetricRowDefinition
from .models import (
    DualMetricRowData,
    MetricsRowsData,
    StandardMetricRowData,
)

def map_standard_metrics_rows(
    *,
    definitions: tuple[StandardMetricRowDefinition, ...],
    kpis: dict[str, Any],
) -> MetricsRowsData:
    filtered_kpis = _reduce_kpi_values(definitions=definitions, kpis=kpis)

    return MetricsRowsData.from_iterable(
        metrics=(
            map_standard_metric_row(
                definition=definition,
                kpis=filtered_kpis,
            )
            for definition in definitions
        )
    )

def map_standard_metric_row(
    *,
    definition: StandardMetricRowDefinition,
    kpis: dict[str, Any],
) -> StandardMetricRowData:
    return StandardMetricRowData(
        label=definition.label,
        value=kpis.get(definition.value_key),
        value_color=kpis.get(definition.value_color_key),
        unit=definition.unit,
        container_class_name=definition.container_class_name,
        font_size_class_name=definition.font_size_class_name,
    )

def map_dual_metrics_rows(
    *,
    definitions: tuple[DualMetricRowDefinition, ...],
    kpis: dict[str, Any],
) -> MetricsRowsData:
    filtered_kpis = _reduce_kpi_values(definitions=definitions, kpis=kpis)

    return MetricsRowsData.from_iterable(
        metrics=(
            map_dual_metric_row(
                definition=definition,
                kpis=filtered_kpis,
            )
            for definition in definitions
        )
    )

def map_dual_metric_row(
    *,
    definition: DualMetricRowDefinition,
    kpis: dict[str, Any],
) -> DualMetricRowData:
    return DualMetricRowData(
        initial_label=definition.initial_label,
        first_label=definition.first_label,
        first_value=kpis.get(definition.first_value_key),
        first_value_color=kpis.get(definition.first_value_color_key),
        first_unit=definition.first_unit,
        divider_value=definition.divider_value,
        second_label=definition.second_label,
        second_value=kpis.get(definition.second_value_key),
        second_value_color=kpis.get(definition.second_value_color_key),
        second_unit=definition.second_unit,
        divider_class_name=definition.divider_class_name,
        container_class_name=definition.container_class_name,
        font_size_class_name=definition.font_size_class_name,
    )

def _reduce_kpi_values(
    *,
    definitions: tuple[Any, ...],
    kpis: dict[str, Any],
) -> dict[str, Any]:
    required_keys = set()

    for definition in definitions:
        for attr_name in dir(definition):
            if not attr_name.endswith('_key'):
                continue

            dict_key = getattr(definition, attr_name)
            if dict_key:
                required_keys.add(dict_key)

    filtered_kpis = {key: kpis[key] for key in required_keys if key in kpis}
    filtered_kpis[''] = kpis.get('')
    return filtered_kpis