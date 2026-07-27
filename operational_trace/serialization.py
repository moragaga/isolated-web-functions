from __future__ import annotations

from .models import OperationalTraceDefinition


def serialize_snapshot(
    *,
    definition: OperationalTraceDefinition,
    version: str,
) -> dict:
    return {
        'version': version,
        'selection_keys': [
            alarm.selection_key
            for alarm in definition.ordered_alarms
        ],
        'alarms': [
            {
                'alarm_id': alarm.alarm_id,
                'selection_key': alarm.selection_key,
                'tone': alarm.tone.value,
                'origin_process_key': alarm.origin_process_key,
                'affected_process_keys': list(alarm.affected_process_keys),
            }
            for alarm in definition.ordered_alarms
        ],
    }
