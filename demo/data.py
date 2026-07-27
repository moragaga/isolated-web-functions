from __future__ import annotations

from operational_trace import (
    AlarmDefinition,
    AlarmTone,
    OperationalTraceDefinition,
    OperationalTraceGroup,
    OperationalTraceMode,
    OperationalTracePoint,
)


PROCESS_POINT = OperationalTracePoint(key='flotacion', label='Flotación')


def build_process_definition(*, revision: int) -> OperationalTraceDefinition:
    torque_occurrence = 'process-torque#2' if revision >= 3 else 'process-torque#1'
    alarms = (
        _alarm(
            alarm_id='process-recovery',
            occurrence_id='process-recovery#1',
            title=f'Recuperación bajo objetivo{_suffix(revision)}',
            criticality='C1',
            active_time='5.1 h',
            tone=AlarmTone.CRITICAL,
            origin='flotacion',
            order=0,
        ),
        _alarm(
            alarm_id='process-grade',
            occurrence_id='process-grade#1',
            title=f'Ley concentrado fuera de rango{_suffix(revision)}',
            criticality='C2',
            active_time='1.3 h',
            tone=AlarmTone.WARNING,
            origin='flotacion',
            order=1,
        ),
        _alarm(
            alarm_id='process-torque',
            occurrence_id=torque_occurrence,
            title=(
                'Nueva ocurrencia de torque TK-10'
                if revision >= 3
                else f'Torque TK-10 requiere atención{_suffix(revision)}'
            ),
            criticality='C2',
            active_time='48 min',
            tone=AlarmTone.WARNING,
            origin='flotacion',
            order=2,
        ),
        _alarm(
            alarm_id='process-flow',
            occurrence_id='process-flow#1',
            title=f'Flujo selectiva bajo objetivo{_suffix(revision)}',
            criticality='C3',
            active_time='22 min',
            tone=AlarmTone.NEUTRAL,
            origin='flotacion',
            order=3,
        ),
    )
    return OperationalTraceDefinition.from_iterables(
        scope_id='process-demo',
        mode=OperationalTraceMode.PROCESS,
        points=(PROCESS_POINT,),
        alarms=alarms,
    )


def build_distributed_definition(*, revision: int) -> OperationalTraceDefinition:
    distributed_two_occurrence = (
        'distributed-central#2'
        if revision >= 3
        else 'distributed-central#1'
    )
    distributed_two_tone = (
        AlarmTone.WARNING
        if revision >= 3
        else AlarmTone.CRITICAL
    )
    normal_alarms = ()
    if revision < 2:
        normal_alarms = (
            _alarm(
                alarm_id='distributed-normal',
                occurrence_id='distributed-normal#1',
                title=f'Disponibilidad bajo objetivo{_suffix(revision)}',
                criticality='C2',
                active_time='55 min',
                tone=AlarmTone.WARNING,
                origin='flotacion',
                order=0,
            ),
        )
    distributed_alarms = (
        _alarm(
            alarm_id='distributed-south',
            occurrence_id='distributed-south#1',
            title='H₂S sector sur',
            criticality='C2',
            active_time='18 min',
            tone=AlarmTone.WARNING,
            origin='flotacion',
            order=1,
            distributed=True,
        ),
        _alarm(
            alarm_id='distributed-central',
            occurrence_id=distributed_two_occurrence,
            title=(
                'Nueva ocurrencia H₂S sector central'
                if revision >= 3
                else 'H₂S sector central'
            ),
            criticality='C1' if revision < 3 else 'C2',
            active_time='24 min',
            tone=distributed_two_tone,
            origin='flotacion',
            order=2,
            distributed=True,
        ),
        _alarm(
            alarm_id='distributed-north',
            occurrence_id='distributed-north#1',
            title='H₂S sector norte',
            criticality='C2',
            active_time='31 min',
            tone=AlarmTone.WARNING,
            origin='flotacion',
            order=3,
            distributed=True,
        ),
    )
    return OperationalTraceDefinition.from_iterables(
        scope_id='distributed-demo',
        mode=OperationalTraceMode.DISTRIBUTED,
        points=(PROCESS_POINT,),
        alarms=(*normal_alarms, *distributed_alarms),
    )


def build_integrated_definition(*, revision: int) -> OperationalTraceDefinition:
    points = (
        OperationalTracePoint(key='general_mina', label='General Mina'),
        OperationalTracePoint(key='carguio', label='Carguío'),
        OperationalTracePoint(key='transporte', label='Transporte'),
        OperationalTracePoint(key='chancado_stmg', label='Chancado-STMG'),
        OperationalTracePoint(key='stock_chacay', label='Stock Chacay'),
        OperationalTracePoint(key='molienda', label='Molienda'),
        OperationalTracePoint(key='flotacion', label='Flotación'),
        OperationalTracePoint(
            key='transporte_fluidos',
            label='Transporte de Fluidos',
        ),
        OperationalTracePoint(key='puerto', label='Puerto'),
    )
    carguio_occurrence = 'io-loading#2' if revision >= 2 else 'io-loading#1'
    carguio_effect = (
        ('transporte', 'chancado_stmg')
        if revision >= 2
        else ('transporte', 'chancado_stmg', 'stock_chacay')
    )
    alarms = (
        _alarm(
            alarm_id='io-mp10',
            occurrence_id='io-mp10#1',
            title=f'MP10 alto{_suffix(revision)}',
            criticality='C2',
            active_time='3.4 h',
            tone=AlarmTone.CRITICAL,
            origin='general_mina',
            order=0,
            group='mine',
        ),
        _alarm(
            alarm_id='io-loading',
            occurrence_id=carguio_occurrence,
            title=(
                'Nueva ocurrencia en Carguío'
                if revision >= 2
                else f'Carguío bajo rendimiento{_suffix(revision)}'
            ),
            criticality='C1',
            active_time='2.1 h',
            tone=AlarmTone.CRITICAL if revision >= 2 else AlarmTone.WARNING,
            origin='carguio',
            affected=carguio_effect,
            order=1,
            group='mine',
        ),
        _alarm(
            alarm_id='io-crushing',
            occurrence_id='io-crushing#1',
            title=f'CH-02 disponibilidad baja{_suffix(revision)}',
            criticality='C2',
            active_time='3.8 h',
            tone=AlarmTone.WARNING,
            origin='chancado_stmg',
            affected=('stock_chacay',),
            order=2,
            group='mine',
        ),
        _alarm(
            alarm_id='io-grinding',
            occurrence_id='io-grinding#1',
            title=f'Molienda limita producción{_suffix(revision)}',
            criticality='C1',
            active_time='52 min',
            tone=AlarmTone.CRITICAL,
            origin='molienda',
            affected=('flotacion',),
            order=3,
            group='plant',
        ),
        _alarm(
            alarm_id='io-recovery',
            occurrence_id='io-recovery#1',
            title=f'Recuperación colectiva baja{_suffix(revision)}',
            criticality='C2',
            active_time='46 min',
            tone=AlarmTone.WARNING,
            origin='flotacion',
            order=4,
            group='plant',
        ),
        _alarm(
            alarm_id='io-port',
            occurrence_id='io-port#1',
            title=f'Puerto requiere atención{_suffix(revision)}',
            criticality='C3',
            active_time='19 min',
            tone=AlarmTone.NEUTRAL,
            origin='puerto',
            order=5,
            group='plant',
        ),
    )
    return OperationalTraceDefinition.from_iterables(
        scope_id='integrated-demo',
        mode=OperationalTraceMode.INTEGRATED_OPERATIONS,
        points=points,
        alarms=alarms,
        groups=(
            OperationalTraceGroup.from_iterable(
                key='mine',
                label='Mina',
                point_keys=tuple(point.key for point in points[:4]),
            ),
            OperationalTraceGroup.from_iterable(
                key='plant',
                label='Planta',
                point_keys=tuple(point.key for point in points[4:]),
            ),
        ),
    )


def resolve_demo_revision(*, n_intervals: int) -> int:
    return min(n_intervals // 3, 3)


def resolve_distributed_active_selection_key(
    *,
    n_intervals: int,
    revision: int,
) -> str:
    central_key = (
        'distributed-central#2'
        if revision >= 3
        else 'distributed-central#1'
    )
    keys = (
        'distributed-south#1',
        central_key,
        'distributed-north#1',
    )
    return keys[(n_intervals // 6) % len(keys)]


def _alarm(
    *,
    alarm_id: str,
    occurrence_id: str,
    title: str,
    criticality: str,
    active_time: str,
    tone: AlarmTone,
    origin: str,
    order: int,
    affected: tuple[str, ...] = (),
    group: str | None = None,
    distributed: bool = False,
) -> AlarmDefinition:
    return AlarmDefinition.from_iterable(
        alarm_id=alarm_id,
        occurrence_id=occurrence_id,
        title=title,
        criticality=criticality,
        active_time=active_time,
        tone=tone,
        origin_process_key=origin,
        affected_process_keys=affected,
        display_order=order,
        placement_group_key=group,
        is_distributed=distributed,
    )


def _suffix(revision: int) -> str:
    return '' if revision == 0 else f' · actualización {revision}'
