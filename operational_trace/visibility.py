from __future__ import annotations

from dataclasses import dataclass

from .enums import OperationalTraceMode
from .models import AlarmDefinition, OperationalTraceDefinition


@dataclass(frozen=True, slots=True)
class AlarmVisibility:
    selectable_selection_keys: tuple[str, ...]
    active_distributed_selection_key: str | None = None


def resolve_alarm_visibility(
    *,
    definition: OperationalTraceDefinition,
    active_distributed_selection_key: str | None = None,
) -> AlarmVisibility:
    ordered_alarms = definition.ordered_alarms
    if definition.mode is not OperationalTraceMode.DISTRIBUTED:
        return AlarmVisibility(
            selectable_selection_keys=tuple(
                alarm.selection_key
                for alarm in ordered_alarms
            ),
        )

    distributed_alarms = tuple(
        alarm
        for alarm in ordered_alarms
        if alarm.is_distributed
    )
    if len(distributed_alarms) <= definition.distributed_threshold:
        return AlarmVisibility(
            selectable_selection_keys=tuple(
                alarm.selection_key
                for alarm in ordered_alarms
            ),
        )

    normal_alarm_keys = tuple(
        alarm.selection_key
        for alarm in ordered_alarms
        if not alarm.is_distributed
    )
    active_key = resolve_active_distributed_selection_key(
        alarms=distributed_alarms,
        active_selection_key=active_distributed_selection_key,
    )
    return AlarmVisibility(
        selectable_selection_keys=(*normal_alarm_keys, active_key),
        active_distributed_selection_key=active_key,
    )


def resolve_active_distributed_selection_key(
    *,
    alarms: tuple[AlarmDefinition, ...],
    active_selection_key: str | None,
) -> str:
    if not alarms:
        raise ValueError('Distributed alarm collection must not be empty.')
    available_keys = {alarm.selection_key for alarm in alarms}
    if active_selection_key in available_keys:
        return active_selection_key
    return alarms[0].selection_key
