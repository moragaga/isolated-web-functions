from __future__ import annotations

import base64
from html import escape

from .geometry import (
    build_irregular_fill_path,
    clamp,
    interpolate_profile,
    render_pile_geometry,
)
from .models import StockpileItem, StockpileMode, StockpilePanel


def build_stockpile_panel_svg(panel: StockpilePanel) -> str:
    width = 920
    header_height = 34
    body_height = 238 if panel.mode is StockpileMode.MINE else 196
    height = header_height + body_height
    cell_width = width / len(panel.items)
    groups = []

    for index, item in enumerate(panel.items):
        groups.append(
            _build_stockpile_group(
                panel=panel,
                item=item,
                index=index,
                cell_x=index * cell_width,
                cell_width=cell_width,
                header_height=header_height,
                body_height=body_height,
            )
        )

    separators = "".join(
        f'<line x1="{cell_width * index:.2f}" y1="{header_height + 8}" '
        f'x2="{cell_width * index:.2f}" y2="{height - 10}" '
        f'stroke="#b7b7b7" stroke-width="1"/>'
        for index in range(1, len(panel.items))
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg"
        width="{width}"
        height="{height}"
        viewBox="0 0 {width} {height}"
        role="img"
        aria-label="{escape(panel.title)}">
        {_build_definitions()}
        <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}"
            rx="5" fill="#e9e9e9" stroke="#bdbdbd"/>
        <rect x="1" y="1" width="{width - 2}" height="{header_height}"
            rx="4" fill="#dedede"/>
        <line x1="1" y1="{header_height}" x2="{width - 1}" y2="{header_height}"
            stroke="#b8b8b8" stroke-width="1"/>
        <text x="14" y="23"
            font-family="Arial, Helvetica, sans-serif"
            font-size="18"
            font-weight="700"
            fill="#3d3d3d">{escape(panel.title)}</text>
        {separators}
        {"".join(groups)}
    </svg>"""


def build_stockpile_data_uri(panel: StockpilePanel) -> str:
    svg = build_stockpile_panel_svg(panel)
    payload = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{payload}"


def _build_definitions() -> str:
    return """
    <defs>
        <pattern id="stockpile-light-texture"
            width="13" height="11"
            patternUnits="userSpaceOnUse">
            <circle cx="2" cy="3" r="0.8" fill="#8f8f8f" opacity="0.46"/>
            <circle cx="9" cy="7" r="1.0" fill="#9b9b9b" opacity="0.38"/>
            <path d="M 4 9 L 7 6 L 11 9"
                fill="none" stroke="#929292" stroke-width="0.65" opacity="0.38"/>
            <path d="M 0 6 L 3 5"
                stroke="#a2a2a2" stroke-width="0.7" opacity="0.45"/>
        </pattern>
        <pattern id="stockpile-dark-texture"
            width="12" height="10"
            patternUnits="userSpaceOnUse">
            <circle cx="3" cy="2" r="0.9" fill="#4f4f4f" opacity="0.42"/>
            <circle cx="9" cy="7" r="0.8" fill="#515151" opacity="0.38"/>
            <path d="M 1 8 L 5 5 L 8 8"
                fill="none" stroke="#4d4d4d" stroke-width="0.75" opacity="0.48"/>
            <path d="M 7 1 L 11 3"
                stroke="#565656" stroke-width="0.7" opacity="0.42"/>
        </pattern>
        <linearGradient id="stockpile-light-volume" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stop-color="#a7a7a7"/>
            <stop offset="39%" stop-color="#d0d0d0"/>
            <stop offset="57%" stop-color="#ececec"/>
            <stop offset="76%" stop-color="#bcbcbc"/>
            <stop offset="100%" stop-color="#989898"/>
        </linearGradient>
        <linearGradient id="stockpile-dark-volume" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stop-color="#666666"/>
            <stop offset="42%" stop-color="#858585"/>
            <stop offset="64%" stop-color="#707070"/>
            <stop offset="100%" stop-color="#5a5a5a"/>
        </linearGradient>
    </defs>
    """


def _build_stockpile_group(
    *,
    panel: StockpilePanel,
    item: StockpileItem,
    index: int,
    cell_x: float,
    cell_width: float,
    header_height: float,
    body_height: float,
) -> str:
    cell_padding = 18
    label_y = header_height + 23
    max_width = cell_width - cell_padding * 2
    pile_width = min(max_width, 350 if panel.mode is StockpileMode.MINE else 190)
    pile_height = 158 if panel.mode is StockpileMode.MINE else 126
    pile_x = cell_x + (cell_width - pile_width) / 2
    pile_y = header_height + body_height - pile_height - 18

    if panel.mode is StockpileMode.MINE:
        height_ratio = clamp((item.height_m or 0) / panel.common_scale_m, 0.0, 1.0)
    else:
        height_ratio = 1.0

    profile = interpolate_profile(height_ratio)
    geometry = render_pile_geometry(
        points=profile,
        x=pile_x,
        y=pile_y,
        width=pile_width,
        height=pile_height,
    )

    visible_height = geometry.base_y - geometry.apex_y
    fill_y = geometry.base_y - visible_height * item.percent / 100
    fill_path = build_irregular_fill_path(
        key=f"{panel.title}:{item.key}:{item.percent:.3f}",
        x=pile_x,
        width=pile_width,
        fill_y=fill_y,
        base_y=geometry.base_y,
    )
    clip_id = f"stockpile-clip-{index}"
    badge_width = 90 if panel.mode is StockpileMode.MINE else 80
    badge_height = 55 if panel.mode is StockpileMode.MINE else 50
    badge_x = geometry.apex_x - badge_width / 2
    badge_y = geometry.base_y - badge_height - 14
    font_size = 23 if panel.mode is StockpileMode.MINE else 19
    font_size = 35 if panel.mode is StockpileMode.MINE else 32

    measurement = ""
    max_label = ""

    if panel.mode is StockpileMode.MINE:
        measurement_y = max(label_y + 22, geometry.apex_y - 8)
        measurement = f"""
        <line x1="{geometry.apex_x:.2f}" y1="{measurement_y + 4:.2f}"
            x2="{geometry.apex_x:.2f}" y2="{geometry.apex_y - 2:.2f}"
            stroke="#6c6c6c" stroke-width="1" stroke-dasharray="3 3"/>
        <text x="{geometry.apex_x:.2f}" y="{measurement_y:.2f}"
            text-anchor="middle"
            font-family="Arial, Helvetica, sans-serif"
            font-size="14"
            font-weight="700"
            fill="#444444">{item.height_m:.1f}m</text>
        """
        max_label = f"""
        <text x="{cell_x + cell_width - 14:.2f}" y="{label_y:.2f}"
            text-anchor="end"
            font-family="Arial, Helvetica, sans-serif"
            font-size="12"
            fill="#555555">Máx. {item.max_height_m:.0f}m</text>
        """

    return f"""
    <g>
        <text x="{cell_x + 14:.2f}" y="{label_y:.2f}"
            font-family="Arial, Helvetica, sans-serif"
            font-size="14"
            font-weight="700"
            fill="#444444">{escape(item.label)}</text>
        {max_label}
        <clipPath id="{clip_id}">
            <path d="{geometry.path}"/>
        </clipPath>
        <path d="{geometry.path}"
            fill="url(#stockpile-light-volume)"
            stroke="#666666"
            stroke-width="1.1"
            stroke-linejoin="round"/>
        <path d="{geometry.path}"
            fill="url(#stockpile-light-texture)"
            opacity="0.72"/>
        <path d="{fill_path}"
            clip-path="url(#{clip_id})"
            fill="url(#stockpile-dark-volume)"/>
        <path d="{fill_path}"
            clip-path="url(#{clip_id})"
            fill="url(#stockpile-dark-texture)"
            opacity="0.78"/>
        <path d="{geometry.path}"
            fill="none"
            stroke="#5e5e5e"
            stroke-width="1.1"
            stroke-linejoin="round"/>
        <rect x="{geometry.base_left_x - 7:.2f}" y="{geometry.base_y - 1:.2f}"
            width="{geometry.base_right_x - geometry.base_left_x + 14:.2f}"
            height="5" rx="1.5"
            fill="#868686" stroke="#5f5f5f" stroke-width="0.8"/>
        {measurement}
        <rect x="{badge_x:.2f}" y="{badge_y:.2f}"
            width="{badge_width}" height="{badge_height}" rx="4"
            fill="#4f4f4f" fill-opacity="0.94"
            stroke="#d6d6d6" stroke-width="1"/>
        <text x="{geometry.apex_x:.2f}" y="{badge_y + badge_height * 0.72:.2f}"
            text-anchor="middle"
            font-family="Arial, Helvetica, sans-serif"
            font-size="{font_size}"
            font-weight="700"
            fill="#f4f4f4">{item.percent:.0f}%</text>
    </g>
    """
