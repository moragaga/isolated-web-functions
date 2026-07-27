from __future__ import annotations

from dataclasses import dataclass

from .enums import OperationalTraceMode
from .models import OperationalTraceDefinition


@dataclass(frozen=True, slots=True)
class AlarmPlacement:
    selection_key: str
    slot_index: int


def resolve_alarm_placements(
    *,
    definition: OperationalTraceDefinition,
) -> dict[str, AlarmPlacement]:
    if definition.mode is OperationalTraceMode.INTEGRATED_OPERATIONS:
        return _resolve_integrated_placements(definition=definition)
    if definition.mode is OperationalTraceMode.DISTRIBUTED:
        return _resolve_distributed_placements(definition=definition)
    return _resolve_process_placements(definition=definition)


def resolve_alarm_slot_count(*, definition: OperationalTraceDefinition) -> int:
    if definition.mode is OperationalTraceMode.INTEGRATED_OPERATIONS:
        return len(definition.points)
    return definition.process_slot_count


def resolve_slot_center_percent(*, slot_index: int, slot_count: int) -> float:
    if slot_count <= 0:
        raise ValueError('Alarm slot count must be greater than zero.')
    if slot_index < 0 or slot_index >= slot_count:
        raise ValueError('Alarm slot index is outside the configured capacity.')
    return ((slot_index + 0.5) / slot_count) * 100


def _resolve_process_placements(
    *,
    definition: OperationalTraceDefinition,
) -> dict[str, AlarmPlacement]:
    return {
        alarm.selection_key: AlarmPlacement(
            selection_key=alarm.selection_key,
            slot_index=index,
        )
        for index, alarm in enumerate(definition.ordered_alarms)
    }


def _resolve_distributed_placements(
    *,
    definition: OperationalTraceDefinition,
) -> dict[str, AlarmPlacement]:
    distributed_alarms = tuple(
        alarm for alarm in definition.ordered_alarms if alarm.is_distributed
    )
    if len(distributed_alarms) <= definition.distributed_threshold:
        return _resolve_process_placements(definition=definition)

    normal_alarms = tuple(
        alarm for alarm in definition.ordered_alarms if not alarm.is_distributed
    )
    placements = {
        alarm.selection_key: AlarmPlacement(
            selection_key=alarm.selection_key,
            slot_index=index,
        )
        for index, alarm in enumerate(normal_alarms)
    }
    isolated_slot_index = definition.process_slot_count - 1
    placements.update(
        {
            alarm.selection_key: AlarmPlacement(
                selection_key=alarm.selection_key,
                slot_index=isolated_slot_index,
            )
            for alarm in distributed_alarms
        }
    )
    return placements


def _resolve_integrated_placements(
    *,
    definition: OperationalTraceDefinition,
) -> dict[str, AlarmPlacement]:
    point_index_by_key = {
        point.key: index
        for index, point in enumerate(definition.points)
    }
    alarms_by_group = {
        group.key: tuple(
            alarm
            for alarm in definition.ordered_alarms
            if alarm.placement_group_key == group.key
        )
        for group in definition.groups
    }
    placements: dict[str, AlarmPlacement] = {}

    for group in definition.groups:
        allowed_indexes = tuple(
            point_index_by_key[point_key]
            for point_key in group.point_keys
        )
        occupied_indexes: set[int] = set()

        for alarm in alarms_by_group[group.key]:
            preferred_index = point_index_by_key[alarm.origin_process_key]
            selected_index = _resolve_nearest_available_index(
                preferred_index=preferred_index,
                allowed_indexes=allowed_indexes,
                occupied_indexes=occupied_indexes,
            )
            placements[alarm.selection_key] = AlarmPlacement(
                selection_key=alarm.selection_key,
                slot_index=selected_index,
            )
            occupied_indexes.add(selected_index)

    return placements


def _resolve_nearest_available_index(
    *,
    preferred_index: int,
    allowed_indexes: tuple[int, ...],
    occupied_indexes: set[int],
) -> int:
    available_indexes = tuple(
        index
        for index in allowed_indexes
        if index not in occupied_indexes
    )
    if not available_indexes:
        raise ValueError('No alarm slot is available in the configured trace group.')
    return min(
        available_indexes,
        key=lambda index: (abs(index - preferred_index), index),
    )
