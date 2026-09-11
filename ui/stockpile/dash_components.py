from __future__ import annotations

from dash import html
from dash.development.base_component import Component

from .models import StockpilePanel
from .svg import build_stockpile_data_uri


def build_stockpile_panel_component(
    panel: StockpilePanel,
    *,
    component_id: str | None = None,
    class_name: str = "stockpile-panel",
) -> Component:
    return html.Img(
        id=component_id,
        src=build_stockpile_data_uri(panel),
        className=class_name,
        alt=panel.title,
    )
