from __future__ import annotations

from typing import Any

from dash import html
from dash.development.base_component import Component

from .models import StockpilePanel, StockpileRenderOptions, StockpileTheme
from .svg import build_stockpile_data_uri


def build_stockpile_component(
    panel: StockpilePanel,
    *,
    component_id: str | None = None,
    class_name: str | None = None,
    theme: StockpileTheme | None = None,
    options: StockpileRenderOptions | None = None,
    style: dict[str, Any] | None = None,
) -> Component:
    resolved_style: dict[str, Any] = {
        'display': 'block',
        'width': '100%',
        'height': 'auto',
    }
    if style:
        resolved_style.update(style)
    return html.Img(
        id=component_id,
        className=class_name,
        src=build_stockpile_data_uri(panel, theme=theme, options=options),
        alt=panel.title,
        draggable=False,
        style=resolved_style,
    )
