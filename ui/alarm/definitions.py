from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

class AlarmTone(StrEnum):
    WARNING = 'warning'
    DANGER = 'danger'

class AlarmVisualization(StrEnum):
    QUEUE_IN_QUEUE = 'queue_in_queue'
    NORMAL_QUEUE = 'normal_queue'

@dataclass(frozen=True, slots=True)
class AlarmDefinition:
    id: str = '' # 00000
    occurrence: str = ''
    name: str = '' # ALARM_TEST
    title: str = '' # X X
    cause: str = ''
    risk_category: str = 'Riesgo' # RIESGO / IMPACTO
    risk_kind: str = 'Productivo'
    business_category: str = '' # Medio Ambiente / Costos / Seguridad y Salud / Productividad
    risk_level: str = '' # C1 / C2 / C3
    tone: AlarmTone = AlarmTone.WARNING
    activity_time: str = ''
    activity_time_unit: str = ''
    order: int = 0
    group: str = ''
    visualization: AlarmVisualization = AlarmVisualization.NORMAL_QUEUE
    distributed: bool = False
    origin: str | None = None
    affected: tuple[str, ...] | None = None
