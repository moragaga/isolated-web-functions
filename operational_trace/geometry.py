from __future__ import annotations

from dataclasses import dataclass

from .models import AlarmDefinition, OperationalTraceDefinition
from .placement import (
    AlarmPlacement,
    resolve_alarm_slot_count,
    resolve_slot_center_percent,
)


@dataclass(frozen=True, slots=True)
class AlarmRouteGeometry:
    selection_key: str
    card_x_percent: float
    trunk_start_x_percent: float
    trunk_end_x_percent: float
    process_x_percents: tuple[float, ...]
    origin_x_percent: float
    has_horizontal_trunk: bool
    is_local_route: bool


def resolve_process_positions(
    *,
    definition: OperationalTraceDefinition,
) -> dict[str, float]:
    if len(definition.points) == 1:
        return {definition.points[0].key: 50.0}
    point_count = len(definition.points)
    return {
        point.key: ((index + 0.5) / point_count) * 100
        for index, point in enumerate(definition.points)
    }


def resolve_alarm_route_geometry(
    *,
    definition: OperationalTraceDefinition,
    alarm: AlarmDefinition,
    placement: AlarmPlacement,
) -> AlarmRouteGeometry:
    process_positions = resolve_process_positions(definition=definition)
    slot_count = resolve_alarm_slot_count(definition=definition)
    card_x_percent = resolve_slot_center_percent(
        slot_index=placement.slot_index,
        slot_count=slot_count,
    )
    process_x_percents = tuple(
        process_positions[key]
        for key in alarm.route_process_keys
    )
    route_x_percents = (card_x_percent, *process_x_percents)
    trunk_start_x_percent = min(route_x_percents)
    trunk_end_x_percent = max(route_x_percents)
    has_horizontal_trunk = (
        trunk_end_x_percent - trunk_start_x_percent
    ) > 0.000001

    return AlarmRouteGeometry(
        selection_key=alarm.selection_key,
        card_x_percent=card_x_percent,
        trunk_start_x_percent=trunk_start_x_percent,
        trunk_end_x_percent=trunk_end_x_percent,
        process_x_percents=process_x_percents,
        origin_x_percent=process_positions[alarm.origin_process_key],
        has_horizontal_trunk=has_horizontal_trunk,
        is_local_route=alarm.is_local_route,
    )
