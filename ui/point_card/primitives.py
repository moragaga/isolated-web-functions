from __future__ import annotations

from dash import html
from dash.development.base_component import Component
from .models import PointCardModel


def build_point(
    *,
    model: PointCardModel,
) -> Component:
    return html.Span(
        className='point-card-module point-card__wrapper--single',
        children=[
            model.to_component()
        ],
    )

def build_points(
    *,
    models: tuple[PointCardModel, ...],
) -> Component:
    return html.Div(
        className='point-card-module point-card__wrapper--group',
        style={'--point-card-slot-count': len(models).__str__()},
        children=[build_point(model=model) for model in models]
    )