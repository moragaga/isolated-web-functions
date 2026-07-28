from __future__ import annotations

from dash.development.base_component import Component

from .models import PointCardModel, PointCardGroupModel
from .primitives import build_point, build_points

def build_point_card(
    *,
    model: PointCardModel,
) -> Component:
    return build_point(model=model)

def build_point_card_group(
    *,
    models: PointCardGroupModel,
) -> Component:
    return build_points(models=models)