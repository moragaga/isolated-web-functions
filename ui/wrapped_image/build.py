from __future__ import annotations

from dash import html
from dash.development.base_component import Component

from .models import WrappedImageModel, WrappedImageGroupModel
from .primitives import build_image


def build_wrapped_image(
    *,
    model: WrappedImageModel,
) -> Component:
    return build_image(model=model)


def build_wrapped_images_group(
    *,
    models: WrappedImageGroupModel,
) -> Component:
    return html.Div(
        className='wrapped-image__images-group wrapped__images-group--{0}'.format(models.images_orientation),
        children=[
            build_image(model=model) for model in models.images
        ]
    )
