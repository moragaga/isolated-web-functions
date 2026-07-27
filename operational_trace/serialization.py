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
        'mode': definition.mode.value,
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
        'preview': {
            'enabled': definition.preview.enabled,
            'reveal_duration_ms': definition.preview.reveal_duration_ms,
            'hold_duration_ms': definition.preview.hold_duration_ms,
            'fade_duration_ms': definition.preview.fade_duration_ms,
            'between_routes_ms': definition.preview.between_routes_ms,
            'cycle_pause_ms': definition.preview.cycle_pause_ms,
            'max_cycle_size': definition.preview.max_cycle_size,
            'keep_single_route_visible': (
                definition.preview.keep_single_route_visible
            ),
            'order_strategy': (
                'left-to-right'
                if definition.mode.value == 'integrated-operations'
                else 'priority'
            ),
        },
        'alarms': [
            {
                'alarm_id': alarm.alarm_id,
                'selection_key': alarm.selection_key,
                'preview_key': alarm.preview_key,
                'route_signature': alarm.route_signature,
                'tone': alarm.tone.value,
                'origin_process_key': alarm.origin_process_key,
                'affected_process_keys': list(alarm.affected_process_keys),
                'display_order': alarm.display_order,
                'is_distributed': alarm.is_distributed,
            }
            for alarm in definition.ordered_alarms
        ],
    }
