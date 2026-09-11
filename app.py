from __future__ import annotations
from flask import Flask
from dash import Dash, html
import dash_bootstrap_components as dbc

from demo import build_demo_layout, register_demo_callbacks
from templates.index_string import get_index_page_string
from test_metrics import component as tm
from test_global_indicator import component as gi
from test_wrapped_image import ch1, chs
from test_card_point import points
from test_stockpile import minas, stock

import sys

from operational_trace.callbacks import register_operational_trace_callbacks

from test_alarms import alarms

print("=" * 40)
print("VERSIÓN DE PYTHON EN EJECUCIÓN:", sys.version)
print("RUTA DEL EJECUTABLE:", sys.executable)
print("=" * 40)

app = Flask(__name__)
with app.app_context():
    app_dash = Dash(
        name=__name__,
        server=app,
        external_stylesheets=[dbc.icons.BOOTSTRAP],
        index_string=get_index_page_string()
    )


    # app_dash.layout = html.Div(
    #     children=[
    #         html.P(
    #             children=['WELCOME TO THE DASHBOARD'],
    #         ),
    #     ]
    # )

    app_dash.layout = html.Div(
        className='d-flex flex-column w-100',
        children=[
            minas,
            stock,
            alarms,
            build_demo_layout(),
            html.Div(
                children=gi
            ),
            html.Div(
                children=ch1,
            ),
            html.Div(
                children=chs,
            ),
            html.Div(
                children=points
            ),
            html.Div(
                children=tm
            )
        ]

    )

    for trace_scope_id in (
            'process-demo',
            'distributed-demo',
            'integrated-demo',
    ):
        register_operational_trace_callbacks(
            app=app_dash,
            scope_id=trace_scope_id,
        )

    register_demo_callbacks(app=app_dash)

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=8050,
        use_reloader=True,
    )
