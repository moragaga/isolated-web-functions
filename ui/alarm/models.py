from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True, slots=True)
class AlarmDataModel:
    id: str # 00000
    occurrence: str
    name: str # ALARM_TEST
    title: str # X X
    cause: str
    risk_category: str # RIESGO / IMPACTO
    risk_kind: str
    business_category: str # Medio Ambiente / Costos / Seguridad y Salud / Productividad
    risk_level: str
    tone: str
    activity_time: str
    activity_time_unit: str
    order: int
    group: str
    visualization: str
    distributed: bool
    origin: str | None
    affected: tuple[str, ...] | None

@dataclass(frozen=True, slots=True)
class AlarmGroupDataModel:
    alarms: tuple[AlarmDataModel, ...]

    @classmethod
    def from_iterable(cls, alarms: Iterable[AlarmDataModel]) -> AlarmGroupDataModel:
        return cls(alarms=tuple(alarms))

    def to_component(self):
        from .build import build_alarms
        return build_alarms(definitions=self)

    def __iter__(self) -> Iterable[AlarmDataModel]:
        return iter(self.alarms)

    def __len__(self) -> int:
        return len(self.alarms)