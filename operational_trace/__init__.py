from __future__ import annotations

from .enums import AlarmTone, OperationalTraceMode
from .models import (
    AlarmDefinition,
    OperationalTraceDefinition,
    OperationalTraceGroup,
    OperationalTracePoint,
)


def build_operational_trace_module(*args, **kwargs):
    from .build import build_operational_trace_module as builder

    return builder(*args, **kwargs)


def register_operational_trace_callbacks(*args, **kwargs):
    from .callbacks import register_operational_trace_callbacks as register

    return register(*args, **kwargs)


__all__ = (
    'AlarmDefinition',
    'AlarmTone',
    'OperationalTraceDefinition',
    'OperationalTraceGroup',
    'OperationalTraceMode',
    'OperationalTracePoint',
    'build_operational_trace_module',
    'register_operational_trace_callbacks',
)
