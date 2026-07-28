from __future__ import annotations

from dash import html
from .primitives import build_alarm
from .models import AlarmGroupDataModel


def build_alarms(
    *,
    definitions: AlarmGroupDataModel,
):
    return html.Div(
        className='alarm__container alarm-module',
        children=[
            build_alarm(model=definition) for definition in definitions
        ]
    )
