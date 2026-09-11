from __future__ import annotations

import base64
from hashlib import sha1
from html import escape

from .geometry import (
    build_smooth_closed_path,
    interpolate_profile,
    profile_top_y,
    scale_profile,
)
from .models import (
    StockpileItem,
    StockpileMode,
    StockpilePanel,
    StockpileRenderOptions,
    StockpileTheme,
)


def build_stockpile_svg(
    panel: StockpilePanel,
    *,
    theme: StockpileTheme | None = None,
    options: StockpileRenderOptions | None = None,
) -> str:
    resolved_theme = theme or StockpileTheme()
    resolved_options = options or StockpileRenderOptions()
    width = _resolve_width(len(panel.items), resolved_options)
    title_height = 48 if resolved_options.show_title else 10
    base_y = resolved_options.height - 58
    max_pile_height = base_y - title_height - 52
    item_markup = ''.join(
        _build_item_markup(
            panel=panel,
            item=item,
            index=index,
            center_x=24
            + resolved_options.cell_width / 2
            + index * (resolved_options.cell_width + resolved_options.gap),
            base_y=base_y,
            max_pile_height=max_pile_height,
            theme=resolved_theme,
            options=resolved_options,
        )
        for index, item in enumerate(panel.items)
    )
    card_markup = _build_card_markup(width, resolved_options.height, resolved_theme) if resolved_options.show_card else ''
    title_markup = (
        f'<text x="24" y="35" font-family="Inter, Arial, sans-serif" '
        f'font-size="24" font-weight="760" fill="{resolved_theme.text_primary}">'
        f'{escape(panel.title)}</text>'
        if resolved_options.show_title
        else ''
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
        f'height="{resolved_options.height}" viewBox="0 0 {width} {resolved_options.height}" '
        f'role="img" aria-label="{escape(panel.title)}">'
        f'{_build_global_defs(resolved_theme)}'
        f'{card_markup}'
        f'{title_markup}'
        f'{item_markup}'
        '</svg>'
    )


def stockpile_svg_to_data_uri(svg: str) -> str:
    encoded = base64.b64encode(svg.encode('utf-8')).decode('ascii')
    return f'data:image/svg+xml;base64,{encoded}'


def build_stockpile_data_uri(
    panel: StockpilePanel,
    *,
    theme: StockpileTheme | None = None,
    options: StockpileRenderOptions | None = None,
) -> str:
    return stockpile_svg_to_data_uri(build_stockpile_svg(panel, theme=theme, options=options))


def _build_item_markup(
    *,
    panel: StockpilePanel,
    item: StockpileItem,
    index: int,
    center_x: float,
    base_y: float,
    max_pile_height: float,
    theme: StockpileTheme,
    options: StockpileRenderOptions,
) -> str:
    ratio = _resolve_shape_ratio(panel, item)
    profile = interpolate_profile(ratio)
    pile_width = options.cell_width - 34
    left = center_x - pile_width / 2
    points = scale_profile(
        profile,
        left=left,
        base_y=base_y,
        width=pile_width,
        max_height=max_pile_height,
    )
    path = build_smooth_closed_path(points)
    top_y = profile_top_y(points)
    visible_height = max(base_y - top_y, 1.0)
    peak_x = min(points, key=lambda point: point[1])[0]
    left_facet = (
        f'{left + pile_width * 0.05:.2f},{base_y:.2f} '
        f'{peak_x - pile_width * 0.03:.2f},{top_y + visible_height * 0.08:.2f} '
        f'{peak_x + pile_width * 0.05:.2f},{top_y + visible_height * 0.22:.2f} '
        f'{left + pile_width * 0.38:.2f},{base_y:.2f}'
    )
    right_facet = (
        f'{peak_x + pile_width * 0.01:.2f},{top_y + visible_height * 0.03:.2f} '
        f'{left + pile_width * 0.92:.2f},{base_y:.2f} '
        f'{left + pile_width * 0.58:.2f},{base_y:.2f} '
        f'{peak_x + pile_width * 0.08:.2f},{top_y + visible_height * 0.25:.2f}'
    )
    fill_height = visible_height * item.percent / 100.0
    fill_y = base_y - fill_height
    identifier = _build_identifier(item.key, index)
    label_y = 72 if options.show_title else 34
    height_markup = _build_height_markup(panel, item, center_x, label_y + 23, theme, options)
    badge_y = base_y - min(max(visible_height * 0.28, 25.0), 44.0)
    shadow_width = max(pile_width * (0.28 + ratio * 0.28), 34.0)
    return (
        f'<defs><clipPath id="clip-{identifier}"><path d="{path}"/></clipPath></defs>'
        f'<text x="{center_x:.2f}" y="{label_y:.2f}" text-anchor="middle" '
        f'font-family="Inter, Arial, sans-serif" font-size="17" font-weight="740" '
        f'fill="{theme.text_primary}">{escape(item.label)}</text>'
        f'{height_markup}'
        f'<ellipse cx="{center_x:.2f}" cy="{base_y + 5:.2f}" rx="{shadow_width:.2f}" ry="9" '
        f'fill="#252b31" opacity="0.16" filter="url(#stockpile-ground-blur)"/>'
        f'<g filter="url(#stockpile-drop-shadow)">'
        f'<path d="{path}" fill="url(#stockpile-pile-gradient)" '
        f'filter="url(#stockpile-mineral-texture)"/>'
        f'<rect x="{left:.2f}" y="{fill_y:.2f}" width="{pile_width:.2f}" '
        f'height="{fill_height:.2f}" fill="url(#stockpile-fill-gradient)" '
        f'clip-path="url(#clip-{identifier})"/>'
        f'<polygon points="{left_facet}" fill="#20262c" opacity="0.11" '
        f'clip-path="url(#clip-{identifier})"/>'
        f'<polygon points="{right_facet}" fill="#ffffff" opacity="0.14" '
        f'clip-path="url(#clip-{identifier})"/>'
        f'<line x1="{left:.2f}" y1="{fill_y:.2f}" x2="{left + pile_width:.2f}" y2="{fill_y:.2f}" '
        f'stroke="#eef0f2" stroke-width="1.3" stroke-opacity="0.55" '
        f'clip-path="url(#clip-{identifier})"/>'
        f'<path d="{path}" fill="url(#stockpile-highlight-gradient)" opacity="0.64"/>'
        f'</g>'
        f'<rect x="{center_x - 31:.2f}" y="{badge_y - 19:.2f}" width="62" height="31" rx="9" '
        f'fill="{theme.badge}" opacity="0.96"/>'
        f'<text x="{center_x:.2f}" y="{badge_y + 3:.2f}" text-anchor="middle" '
        f'font-family="Inter, Arial, sans-serif" font-size="18" font-weight="780" '
        f'fill="{theme.badge_text}">{_format_percentage(item.percent)}</text>'
        f'<rect x="{left + 8:.2f}" y="{base_y + 12:.2f}" width="{pile_width - 16:.2f}" '
        f'height="4" rx="2" fill="{theme.track}" opacity="0.82"/>'
    )


def _build_height_markup(
    panel: StockpilePanel,
    item: StockpileItem,
    center_x: float,
    y: float,
    theme: StockpileTheme,
    options: StockpileRenderOptions,
) -> str:
    if panel.mode is StockpileMode.FIXED_PERCENTAGE:
        return ''
    current = _format_meters(item.height_m)
    maximum = _format_meters(item.max_height_m)
    maximum_markup = (
        f'<text x="{center_x:.2f}" y="{y + 18:.2f}" text-anchor="middle" '
        f'font-family="Inter, Arial, sans-serif" font-size="12" font-weight="560" '
        f'fill="{theme.text_secondary}">máx. {maximum}</text>'
        if options.show_item_maximum
        else ''
    )
    return (
        f'<text x="{center_x:.2f}" y="{y:.2f}" text-anchor="middle" '
        f'font-family="Inter, Arial, sans-serif" font-size="18" font-weight="760" '
        f'fill="{theme.text_primary}">{current}</text>'
        f'{maximum_markup}'
    )


def _resolve_shape_ratio(panel: StockpilePanel, item: StockpileItem) -> float:
    if panel.mode is StockpileMode.FIXED_PERCENTAGE:
        return 1.0
    scale = panel.resolved_common_scale_max_m
    if scale is None or item.height_m is None:
        raise ValueError('Mine stockpile scale and height are required')
    return item.height_m / scale


def _resolve_width(item_count: int, options: StockpileRenderOptions) -> int:
    return 48 + item_count * options.cell_width + max(item_count - 1, 0) * options.gap


def _build_identifier(key: str, index: int) -> str:
    digest = sha1(f'{index}:{key}'.encode('utf-8')).hexdigest()[:10]
    return f'{index}-{digest}'


def _format_percentage(value: float) -> str:
    rounded = round(value, 1)
    if rounded.is_integer():
        return f'{int(rounded)}%'
    return f'{rounded:.1f}%'.replace('.', ',')


def _format_meters(value: float | None) -> str:
    if value is None:
        raise ValueError('Stockpile meter value is required')
    rounded = round(value, 1)
    if rounded.is_integer():
        return f'{int(rounded)} m'
    return f'{rounded:.1f} m'.replace('.', ',')


def _build_card_markup(width: int, height: int, theme: StockpileTheme) -> str:
    return (
        f'<rect x="8" y="8" width="{width - 16}" height="{height - 16}" rx="19" '
        f'fill="url(#stockpile-card-gradient)" filter="url(#stockpile-card-shadow)"/>'
    )


def _build_global_defs(theme: StockpileTheme) -> str:
    return (
        '<defs>'
        f'<linearGradient id="stockpile-card-gradient" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0%" stop-color="{theme.card_start}"/>'
        f'<stop offset="100%" stop-color="{theme.card_end}"/>'
        '</linearGradient>'
        f'<linearGradient id="stockpile-pile-gradient" x1="0" y1="0" x2="1" y2="0.85">'
        f'<stop offset="0%" stop-color="{theme.pile_dark}"/>'
        f'<stop offset="48%" stop-color="{theme.pile_mid}"/>'
        f'<stop offset="76%" stop-color="{theme.pile_light}"/>'
        f'<stop offset="100%" stop-color="{theme.pile_dark}"/>'
        '</linearGradient>'
        f'<linearGradient id="stockpile-fill-gradient" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{theme.fill_top}"/>'
        f'<stop offset="100%" stop-color="{theme.fill_bottom}"/>'
        '</linearGradient>'
        '<radialGradient id="stockpile-highlight-gradient" cx="63%" cy="24%" r="73%">'
        '<stop offset="0%" stop-color="#ffffff" stop-opacity="0.48"/>'
        '<stop offset="58%" stop-color="#ffffff" stop-opacity="0.09"/>'
        '<stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>'
        '</radialGradient>'
        '<filter id="stockpile-card-shadow" x="-20%" y="-20%" width="140%" height="150%">'
        '<feDropShadow dx="0" dy="5" stdDeviation="7" flood-color="#111820" flood-opacity="0.13"/>'
        '</filter>'
        '<filter id="stockpile-drop-shadow" x="-20%" y="-20%" width="140%" height="150%">'
        '<feDropShadow dx="0" dy="5" stdDeviation="4" flood-color="#111820" flood-opacity="0.19"/>'
        '</filter>'
        '<filter id="stockpile-ground-blur" x="-20%" y="-80%" width="140%" height="260%">'
        '<feGaussianBlur stdDeviation="6"/>'
        '</filter>'
        '<filter id="stockpile-mineral-texture" x="-12%" y="-12%" width="124%" height="124%">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.075" numOctaves="3" seed="12" result="noise"/>'
        '<feColorMatrix in="noise" type="matrix" values="0.55 0 0 0 0.2 0 0.55 0 0 0.2 0 0 0.55 0 0.2 0 0 0 0.15 0" result="softNoise"/>'
        '<feBlend in="SourceGraphic" in2="softNoise" mode="multiply"/>'
        '</filter>'
        '</defs>'
    )
