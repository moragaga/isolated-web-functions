from __future__ import annotations

from typing import Any

from .definitions import IndicatorDefinition, GlobalIndicatorDefinition
from .models import IndicatorData, GlobalIndicatorData, GlobalIndicatorsData


def map_indicator_data(
    *,
    indicator: IndicatorDefinition,
    kpis: dict[str, Any],
) -> IndicatorData:
    return IndicatorData(
        real_value=kpis.get(indicator.real_kpi_key),
        color_value=kpis.get(indicator.color_kpi_key),
        temporality=indicator.temporality_label,
        plan_value=kpis.get(indicator.plan_kpi_key),
        only_last_measurement=indicator.only_last_measurement,
    )

def map_global_indicator_data(
    *,
    definition: GlobalIndicatorDefinition,
    kpis: dict[str, Any],
) -> GlobalIndicatorData:
    return GlobalIndicatorData.from_iterable(
        label=definition.label,
        unit=definition.unit,
        indicators=(
            map_indicator_data(
                indicator=indicator,
                kpis=kpis,
            )
            for indicator in definition.indicators
        )
    )

def map_global_indicators_data(
    *,
    definitions: tuple[GlobalIndicatorDefinition, ...],
    kpis: dict[str, Any],
) -> GlobalIndicatorsData:
    return GlobalIndicatorsData.from_iterable(
        components=(
            map_global_indicator_data(
                definition=definition,
                kpis=kpis,
            )
            for definition in definitions
        )
    )