from __future__ import annotations

from dash.development.base_component import Component
from dash import html

from .models import WrappedImageModel


def build_image(
    *,
    model: WrappedImageModel,
) -> Component:
    return html.Div(
        className='wrapped-image__wrapper wrapped_image__position--{0}'.format(model.label_position),
        children=[
            html.P(
                className='wrapped-image__label--properties {0}'.format(model.label_font_size),
                children=[model.label],
            ),
            _safe_image(
                name=model.image,
                state=model.variant if not model.override_state.state else model.override_state.state
            )
        ]
    )


def _safe_image(
    *,
    name: str,
    state: str,
) -> Component:
    if isinstance(state, Component):
        return state

    return html.Img(
        className='wrapped-image__image--properties wrapped_image__image--{0}'.format(name),
        src='assets/img/industrial/{0}/{1}.svg'.format(name, state),
    )