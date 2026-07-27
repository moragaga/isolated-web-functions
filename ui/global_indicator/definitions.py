from __future__ import annotations

from dataclasses import dataclass
import unicodedata

def _remove_accent(*, text: str):
    return ''.join(letter for letter in unicodedata.normalize('NFD', text) if unicodedata.category(letter) != 'Mn')

@dataclass(frozen=True, slots=True)
class IndicatorDefinition:
    temporality: str
    indicator_key: str
    only_last_measurement: bool = False

    @property
    def temporality_key(self) -> str:
        return _remove_accent(text=self.temporality).lower()

    @property
    def temporality_label(self) -> str:
        return self.temporality.capitalize()

    @property
    def real_kpi_key(self) -> str:
        return f'{self.indicator_key}_{self.temporality_key}_real_inst'

    @property
    def plan_kpi_key(self) -> str:
        return f'{self.indicator_key}_{self.temporality_key}_plan_inst'

    @property
    def color_kpi_key(self) -> str:
        return f'{self.indicator_key}_{self.temporality_key}_color_inst'

@dataclass(frozen=True, slots=True)
class IndicatorPropertiesDefinition:
    label: int
    temporality: str
    real_value: str
    plan_value: str
    last_measurement_label: str
    last_measurement_value: str

@dataclass(frozen=True, slots=True)
class GlobalIndicatorDefinition:
    label: str
    unit: str
    properties: IndicatorPropertiesDefinition
    indicators: tuple[IndicatorDefinition, ...]
