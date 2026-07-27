from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from .enums import AlarmTone, OperationalTraceMode


@dataclass(frozen=True, slots=True)
class OperationalTracePoint:
    key: str
    label: str

    def __post_init__(self) -> None:
        if not self.key.strip():
            raise ValueError('Process key must not be empty.')
        if not self.label.strip():
            raise ValueError('Process label must not be empty.')


@dataclass(frozen=True, slots=True)
class OperationalTraceGroup:
    key: str
    label: str
    point_keys: tuple[str, ...]
    max_visible_alarm_count: int = 3

    @classmethod
    def from_iterable(
        cls,
        *,
        key: str,
        label: str,
        point_keys: Iterable[str],
        max_visible_alarm_count: int = 3,
    ) -> OperationalTraceGroup:
        return cls(
            key=key,
            label=label,
            point_keys=tuple(point_keys),
            max_visible_alarm_count=max_visible_alarm_count,
        )

    def __post_init__(self) -> None:
        if not self.key.strip():
            raise ValueError('Trace group key must not be empty.')
        if not self.label.strip():
            raise ValueError('Trace group label must not be empty.')
        if not self.point_keys:
            raise ValueError('Trace group must contain at least one process.')
        if any(not key.strip() for key in self.point_keys):
            raise ValueError('Trace group process keys must not be empty.')
        if len(set(self.point_keys)) != len(self.point_keys):
            raise ValueError('Trace group process keys must be unique.')
        if self.max_visible_alarm_count <= 0:
            raise ValueError('Trace group alarm capacity must be greater than zero.')
        if self.max_visible_alarm_count > len(self.point_keys):
            raise ValueError('Trace group alarm capacity must not exceed its process count.')


@dataclass(frozen=True, slots=True)
class AlarmDefinition:
    alarm_id: str
    occurrence_id: str
    title: str
    criticality: str
    active_time: str
    tone: AlarmTone
    origin_process_key: str
    affected_process_keys: tuple[str, ...]
    display_order: int
    placement_group_key: str | None = None
    is_distributed: bool = False

    @classmethod
    def from_iterable(
        cls,
        *,
        alarm_id: str,
        occurrence_id: str | None,
        title: str,
        criticality: str,
        active_time: str,
        tone: AlarmTone,
        origin_process_key: str,
        affected_process_keys: Iterable[str] = (),
        display_order: int,
        placement_group_key: str | None = None,
        is_distributed: bool = False,
    ) -> AlarmDefinition:
        return cls(
            alarm_id=alarm_id,
            occurrence_id=occurrence_id or alarm_id,
            title=title,
            criticality=criticality,
            active_time=active_time,
            tone=tone,
            origin_process_key=origin_process_key,
            affected_process_keys=tuple(affected_process_keys),
            display_order=display_order,
            placement_group_key=placement_group_key,
            is_distributed=is_distributed,
        )

    def __post_init__(self) -> None:
        if not self.alarm_id.strip():
            raise ValueError('Alarm id must not be empty.')
        if not self.occurrence_id.strip():
            raise ValueError('Alarm occurrence id must not be empty.')
        if not self.title.strip():
            raise ValueError('Alarm title must not be empty.')
        if not self.criticality.strip():
            raise ValueError('Alarm criticality must not be empty.')
        if not self.active_time.strip():
            raise ValueError('Alarm active time must not be empty.')
        if not self.origin_process_key.strip():
            raise ValueError('Alarm origin process key must not be empty.')
        if any(not key.strip() for key in self.affected_process_keys):
            raise ValueError('Alarm affected process keys must not be empty.')
        if len(set(self.affected_process_keys)) != len(self.affected_process_keys):
            raise ValueError('Alarm affected process keys must be unique.')
        if self.origin_process_key in self.affected_process_keys:
            raise ValueError('Alarm affected process keys must not repeat the origin process.')
        if self.display_order < 0:
            raise ValueError('Alarm display order must be greater than or equal to zero.')
        if self.placement_group_key is not None and not self.placement_group_key.strip():
            raise ValueError('Alarm placement group key must not be empty.')

    @property
    def selection_key(self) -> str:
        return self.occurrence_id

    @property
    def route_process_keys(self) -> tuple[str, ...]:
        return (self.origin_process_key, *self.affected_process_keys)

    @property
    def is_local_route(self) -> bool:
        return not self.affected_process_keys


@dataclass(frozen=True, slots=True)
class OperationalTraceDefinition:
    scope_id: str
    mode: OperationalTraceMode
    points: tuple[OperationalTracePoint, ...]
    alarms: tuple[AlarmDefinition, ...]
    groups: tuple[OperationalTraceGroup, ...] = ()
    process_slot_count: int = 6
    distributed_threshold: int = 2

    @classmethod
    def from_iterables(
        cls,
        *,
        scope_id: str,
        mode: OperationalTraceMode,
        points: Iterable[OperationalTracePoint],
        alarms: Iterable[AlarmDefinition],
        groups: Iterable[OperationalTraceGroup] = (),
        process_slot_count: int = 6,
        distributed_threshold: int = 2,
    ) -> OperationalTraceDefinition:
        return cls(
            scope_id=scope_id,
            mode=mode,
            points=tuple(points),
            alarms=tuple(alarms),
            groups=tuple(groups),
            process_slot_count=process_slot_count,
            distributed_threshold=distributed_threshold,
        )

    def __post_init__(self) -> None:
        if not self.scope_id.strip():
            raise ValueError('Trace scope id must not be empty.')
        if not self.points:
            raise ValueError('Operational trace must contain at least one process.')
        if self.process_slot_count <= 0:
            raise ValueError('Process alarm slot count must be greater than zero.')
        if self.distributed_threshold < 0:
            raise ValueError('Distributed alarm threshold must be greater than or equal to zero.')

        point_keys = tuple(point.key for point in self.points)
        if len(set(point_keys)) != len(point_keys):
            raise ValueError('Operational trace process keys must be unique.')

        selection_keys = tuple(alarm.selection_key for alarm in self.alarms)
        if len(set(selection_keys)) != len(selection_keys):
            raise ValueError('Operational trace alarm occurrence ids must be unique.')

        point_key_set = set(point_keys)
        for alarm in self.alarms:
            if alarm.origin_process_key not in point_key_set:
                raise ValueError('Alarm origin process key is unknown.')
            unknown_keys = set(alarm.affected_process_keys) - point_key_set
            if unknown_keys:
                raise ValueError('Alarm affected process key is unknown.')

        if self.mode is OperationalTraceMode.INTEGRATED_OPERATIONS:
            self._validate_integrated_operations(point_keys=point_keys)
        else:
            self._validate_single_process_mode()

    def _validate_single_process_mode(self) -> None:
        if len(self.points) != 1:
            raise ValueError('Process and distributed modes require exactly one process point.')
        if self.groups:
            raise ValueError('Process and distributed modes must not define trace groups.')
        if any(alarm.placement_group_key is not None for alarm in self.alarms):
            raise ValueError('Process and distributed alarms must not define a placement group.')

        distributed_count = sum(alarm.is_distributed for alarm in self.alarms)
        visible_alarm_count = len(self.alarms)
        if (
            self.mode is OperationalTraceMode.DISTRIBUTED
            and distributed_count > self.distributed_threshold
        ):
            visible_alarm_count = len(self.alarms) - distributed_count + 1

        if visible_alarm_count > self.process_slot_count:
            raise ValueError('Visible alarm count exceeds the configured process slot capacity.')
        if self.mode is OperationalTraceMode.PROCESS and distributed_count:
            raise ValueError('Process mode must not contain distributed alarms.')

    def _validate_integrated_operations(self, *, point_keys: tuple[str, ...]) -> None:
        if len(self.points) < 2:
            raise ValueError('Integrated operations mode requires at least two process points.')
        if not self.groups:
            raise ValueError('Integrated operations mode requires trace groups.')

        group_keys = tuple(group.key for group in self.groups)
        if len(set(group_keys)) != len(group_keys):
            raise ValueError('Integrated operations group keys must be unique.')

        grouped_point_keys = tuple(
            point_key
            for group in self.groups
            for point_key in group.point_keys
        )
        if len(set(grouped_point_keys)) != len(grouped_point_keys):
            raise ValueError('Integrated operations groups must not overlap.')
        if set(grouped_point_keys) != set(point_keys):
            raise ValueError('Integrated operations groups must partition every process point.')

        group_by_key = {group.key: group for group in self.groups}
        alarm_count_by_group = {group.key: 0 for group in self.groups}

        for alarm in self.alarms:
            if alarm.placement_group_key is None:
                raise ValueError('Integrated operations alarms require a placement group.')
            if alarm.placement_group_key not in group_by_key:
                raise ValueError('Integrated operations alarm placement group is unknown.')
            if alarm.is_distributed:
                raise ValueError('Integrated operations alarms must not be distributed.')

            group = group_by_key[alarm.placement_group_key]
            if alarm.origin_process_key not in group.point_keys:
                raise ValueError('Integrated alarm origin must belong to its placement group.')
            alarm_count_by_group[group.key] += 1

        for group in self.groups:
            if alarm_count_by_group[group.key] > group.max_visible_alarm_count:
                raise ValueError('Integrated operations group alarm capacity was exceeded.')

    @property
    def ordered_alarms(self) -> tuple[AlarmDefinition, ...]:
        return tuple(sorted(self.alarms, key=lambda alarm: alarm.display_order))
