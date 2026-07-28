from __future__ import annotations

from dash import html
import dash_bootstrap_components as dbc
from .models import AlarmDataModel

def build_alarm(
    *,
    model: AlarmDataModel,
):
    text_color = f'alarm__text--{model.tone}'
    background_color = f'alarm__background--{model.tone}'
    border_color = f'alarm__border--{model.tone}'

    return dbc.Card(
        className='alarm-card {0}'.format(border_color),
        children=[
            _header(
                risk_category=model.risk_category,
                business_category=model.business_category,
                risk_level=model.risk_level,
                background_class_name=background_color,
                text_color=text_color
            ),
            _body(
                title=model.title,
                cause=model.cause,
            ),
            _footer(
                activity_time=model.activity_time,
                activity_time_unit=model.activity_time_unit,
            )
        ]
    )

def _header(
    *,
    risk_category: str | None = None,
    business_category: str | None = None,
    risk_level: str | None = None,
    background_class_name: str = '',
    text_color: str = '',
    risk_kind: str = '',
):
    risk_category = risk_category or ''
    business_category = business_category or ''
    risk_level = risk_level or ''
    words = business_category.lower().split(' ')
    src_image = '-'.join(word for word in words if word.strip() != 'y')

    return dbc.CardHeader(
        className='alarm-card__header {0}'.format(background_class_name),
        children=[
            html.Span(
                className='alarm_card__header--risk',
                children=[
                    _safe_img(value=src_image, variant='light'),
                    html.P(
                        className='alarm-card__header--risk-category',
                        children=[f'{risk_category} · {business_category}'],
                    ),
                ]
            ),
            html.P(
                className='alarm-card__header--risk-level {0}'.format(text_color),
                children=[
                    risk_level.upper()
                ]
            )
        ]
    )

def _body(
    *,
    title: str | None = None,
    cause: str | None = None,
):
    title = title or ''
    cause = cause or ''
    return dbc.CardBody(
        className='alarm-card__body',
        children=[
            html.Span(
                className='alarm-card__body--title',
                children=[html.P(children=[title])],
            ),
            html.Span(
                className='alarm-card__body--cause',
                children=[html.P(children=[cause])]
            )
        ]
    )

def _footer(
    *,
    activity_time: str | None = None,
    activity_time_unit: str | None = None,
):
    activity_time = activity_time or ''
    activity_time_unit = activity_time_unit or ''
    return dbc.CardFooter(
        className='alarm-card__footer',
        children=[
            html.Span(
                className='alarm-card__footer--activity-time',
                children=[html.P(children=[f'>{activity_time}{activity_time_unit}'])],
            ),
            html.Span(
                className='alarm-card__footer--actions',
                children=[
                    html.Button(
                        className='alarm-card__footer-button alarm-card__footer-button--information',
                        type='button',
                        children=['Información']
                    ),
                    html.Button(
                        className='alarm-card__footer-button alarm-card__footer-button--managed',
                        type='button',
                        children=['Gestionar']
                    )
                ]
            )
        ]
    )

def _safe_img(
    *,
    value: str | None = None,
    variant: str | None = None,
):
    if value is None or variant is None:
        return ''

    return html.Img(
        className='img-fluid business-img',
        src='assets/img/icons/{0}/{1}.svg'.format(value, variant),
    )

