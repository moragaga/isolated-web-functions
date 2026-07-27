from __future__ import annotations

from .models import OperationalTraceDefinition
from .visibility import resolve_alarm_visibility


def serialize_snapshot(
    *,
    definition: OperationalTraceDefinition,
    version: str,
    active_distributed_selection_key: str | None = None,
) -> dict:
    visibility = resolve_alarm_visibility(
        definition=definition,
        active_distributed_selection_key=(
            active_distributed_selection_key
        ),
    )
    return {
        'version': version,
        'selection_keys': [
            alarm.selection_key
            for alarm in definition.ordered_alarms
        ],
        'selectable_selection_keys': list(
            visibility.selectable_selection_keys
        ),
        'active_distributed_selection_key': (
            visibility.active_distributed_selection_key
        ),
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
