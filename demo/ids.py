from __future__ import annotations


class DemoIds:
    INTERVAL = 'operational-trace-demo-interval'

    @staticmethod
    def status(scope_id: str) -> str:
        return f'{scope_id}-demo-status'
