# from __future__ import annotations
#
# from dash import html
#
# from ui.stockpiles import (
#     StockpileItem,
#     StockpileMode,
#     StockpilePanel,
#     build_stockpile_data_uri,
# )
#
# mina = [
#     {'key': 'mine-1', 'label': 'Pila 1', 'percent': 56, 'height_m': 16, 'max_height_m': 30},
#     {'key': 'mine-2', 'label': 'Pila 2', 'percent': 80, 'height_m': 25, 'max_height_m': 26},
# ]
#
# mine_panel = StockpilePanel(
#         title='Stockpile Mina',
#         mode=StockpileMode.MINE,
#         common_scale_max_m=30,
#         items=tuple(StockpileItem(**item) for item in mina),
#     )
#
# stockpile = html.Img(src=build_stockpile_data_uri(mine_panel))

from __future__ import annotations

from dash import Dash, Input, Output, callback, dcc, html

from ui.stockpile.models import (
    StockpileItem,
    StockpileMode,
    StockpilePanel,
)
from ui.stockpile.dash_components import (
    build_stockpile_data_uri,
    build_stockpile_panel_component,
)


def build_mine_panel(
    *,
    pile_1_height: float,
    pile_1_percent: float,
    pile_2_height: float,
    pile_2_percent: float,
) -> StockpilePanel:
    return StockpilePanel(
        title="Stockpile Mina",
        mode=StockpileMode.MINE,
        common_scale_m=30,
        items=(
            StockpileItem(
                key="mine-1",
                label="Pila 1",
                height_m=pile_1_height,
                max_height_m=30,
                percent=pile_1_percent,
            ),
            StockpileItem(
                key="mine-2",
                label="Pila 2",
                height_m=pile_2_height,
                max_height_m=26,
                percent=pile_2_percent,
            ),
        ),
    )


def build_chacay_panel(
    *,
    pile_a_percent: float,
    pile_b_percent: float,
    pile_c_percent: float,
    pile_d_percent: float,
) -> StockpilePanel:
    return StockpilePanel(
        title="Stockpile Chacay",
        mode=StockpileMode.FIXED,
        items=(
            StockpileItem(key="chacay-a", label="Pila A", percent=pile_a_percent),
            StockpileItem(key="chacay-b", label="Pila B", percent=pile_b_percent),
            StockpileItem(key="chacay-c", label="Pila C", percent=pile_c_percent),
            StockpileItem(key="chacay-d", label="Pila D", percent=pile_d_percent),
        ),
    )


app = Dash(__name__)
app.title = "ADA Stockpiles"

initial_mine = build_mine_panel(
    pile_1_height=15,
    pile_1_percent=10,
    pile_2_height=25,
    pile_2_percent=90,
)
initial_chacay = build_chacay_panel(
    pile_a_percent=78,
    pile_b_percent=35,
    pile_c_percent=0,
    pile_d_percent=91,
)


minas = build_stockpile_panel_component(
    initial_mine,
    component_id="mine-stockpile",
)
stock = build_stockpile_panel_component(
    initial_chacay,
    component_id="chacay-stockpile",
)