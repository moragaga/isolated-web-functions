from __future__ import annotations

from enum import Enum


class OperationalTraceMode(str, Enum):
    PROCESS = 'process'
    DISTRIBUTED = 'distributed'
    INTEGRATED_OPERATIONS = 'integrated-operations'


class AlarmTone(str, Enum):
    CRITICAL = 'critical'
    WARNING = 'warning'
    NEUTRAL = 'neutral'
