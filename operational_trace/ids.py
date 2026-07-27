from __future__ import annotations


class OperationalTraceIds:
    @staticmethod
    def snapshot_store(scope_id: str) -> str:
        return f'{scope_id}-operational-trace-snapshot-store'

    @staticmethod
    def selection_store(scope_id: str) -> str:
        return f'{scope_id}-operational-trace-selection-store'

    @staticmethod
    def module(scope_id: str) -> str:
        return f'{scope_id}-operational-trace-module'

    @staticmethod
    def root(scope_id: str) -> str:
        return f'{scope_id}-operational-trace-root'

    @staticmethod
    def board(scope_id: str) -> str:
        return f'{scope_id}-operational-trace-board'

    @staticmethod
    def route_layer(scope_id: str) -> str:
        return f'{scope_id}-operational-trace-route-layer'

    @staticmethod
    def point_layer(scope_id: str) -> str:
        return f'{scope_id}-operational-trace-point-layer'

    @staticmethod
    def alarm_selector(
        *,
        scope_id: str,
        selection_key: str,
    ) -> dict:
        return {
            'type': 'operational-trace-alarm-selector',
            'scope': scope_id,
            'alarm': selection_key,
        }

    @staticmethod
    def alarm_selector_pattern(
        *,
        scope_id: str,
        alarm,
    ) -> dict:
        return {
            'type': 'operational-trace-alarm-selector',
            'scope': scope_id,
            'alarm': alarm,
        }

    @staticmethod
    def route(
        *,
        scope_id: str,
        selection_key: str,
    ) -> dict:
        return {
            'type': 'operational-trace-route',
            'scope': scope_id,
            'alarm': selection_key,
        }

    @staticmethod
    def route_pattern(
        *,
        scope_id: str,
        alarm,
    ) -> dict:
        return {
            'type': 'operational-trace-route',
            'scope': scope_id,
            'alarm': alarm,
        }

    @staticmethod
    def marker(
        *,
        scope_id: str,
        selection_key: str,
        process_key: str,
    ) -> dict:
        return {
            'type': 'operational-trace-marker',
            'scope': scope_id,
            'alarm': selection_key,
            'process': process_key,
        }

    @staticmethod
    def marker_pattern(
        *,
        scope_id: str,
        alarm,
        process,
    ) -> dict:
        return {
            'type': 'operational-trace-marker',
            'scope': scope_id,
            'alarm': alarm,
            'process': process,
        }
