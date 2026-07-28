from __future__ import annotations

from .models import AlarmDataModel, AlarmGroupDataModel
from .definitions import AlarmDefinition

def map_alarm(
    *,
    definition: AlarmDefinition,
) -> AlarmDataModel:
    if definition.visualization == 'queue_in_queue' and definition.distributed:
        raise 'Visualization not supported, queue_in_queue not accept distributed alarm'

    return AlarmDataModel(
        id=definition.id,
        occurrence=definition.occurrence,
        name=definition.name,
        title=definition.title,
        cause=definition.cause,
        risk_category=definition.risk_category,
        risk_kind=definition.risk_kind,
        business_category=definition.business_category,
        risk_level=definition.risk_level,
        tone=definition.tone,
        activity_time=definition.activity_time,
        activity_time_unit=definition.activity_time_unit,
        order=definition.order,
        group=definition.group,
        visualization=definition.visualization,
        distributed=definition.distributed,
        origin=definition.origin,
        affected=definition.affected,
    )

def map_alarm_group(
    *,
    definitions: tuple[AlarmDefinition, ...],
) -> AlarmGroupDataModel:
    return AlarmGroupDataModel.from_iterable(
        alarms=(
            map_alarm(
                definition=definition
            )
            for definition in definitions
        )
    )