from __future__ import annotations
from flask import Flask
from dash import Dash, html
import dash_bootstrap_components as dbc

from demo import build_demo_layout, register_demo_callbacks
from test_metrics import component as tm
from test_global_indicator import component as gi

import sys

from operational_trace.callbacks import register_operational_trace_callbacks

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
    )


    # app_dash.layout = html.Div(
    #     children=[
    #         html.P(
    #             children=['WELCOME TO THE DASHBOARD'],
    #         ),
    #     ]
    # )

    app_dash.layout = build_demo_layout()

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
