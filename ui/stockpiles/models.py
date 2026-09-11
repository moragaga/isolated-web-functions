from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from math import isfinite


class StockpileMode(StrEnum):
    MINE = 'mine'
    FIXED_PERCENTAGE = 'fixed_percentage'


@dataclass(frozen=True, slots=True)
class StockpileItem:
    key: str
    label: str
    percent: float
    height_m: float | None = None
    max_height_m: float | None = None

    def __post_init__(self) -> None:
        if not self.key.strip():
            raise ValueError('Stockpile key must not be empty')
        if not self.label.strip():
            raise ValueError('Stockpile label must not be empty')
        if not isfinite(self.percent) or not 0 <= self.percent <= 100:
            raise ValueError('Stockpile percent must be between 0 and 100')
        if (self.height_m is None) != (self.max_height_m is None):
            raise ValueError('Stockpile height and maximum height must be provided together')
        if self.height_m is None:
            return
        if not isfinite(self.height_m) or self.height_m < 0:
            raise ValueError('Stockpile height must be greater than or equal to zero')
        if not isfinite(self.max_height_m) or self.max_height_m <= 0:
            raise ValueError('Stockpile maximum height must be greater than zero')
        if self.height_m > self.max_height_m:
            raise ValueError('Stockpile height must not exceed its maximum height')


@dataclass(frozen=True, slots=True)
class StockpilePanel:
    title: str
    mode: StockpileMode
    items: tuple[StockpileItem, ...]
    common_scale_max_m: float | None = None

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError('Stockpile panel title must not be empty')
        if not self.items:
            raise ValueError('Stockpile panel must contain at least one item')
        keys = [item.key for item in self.items]
        if len(keys) != len(set(keys)):
            raise ValueError('Stockpile item keys must be unique')
        if self.mode is StockpileMode.MINE:
            self._validate_mine_mode()
        else:
            self._validate_fixed_percentage_mode()

    @property
    def resolved_common_scale_max_m(self) -> float | None:
        if self.mode is StockpileMode.FIXED_PERCENTAGE:
            return None
        if self.common_scale_max_m is not None:
            return self.common_scale_max_m
        return max(item.max_height_m for item in self.items if item.max_height_m is not None)

    def _validate_mine_mode(self) -> None:
        if any(item.height_m is None for item in self.items):
            raise ValueError('Mine stockpiles require height and maximum height values')
        maximum_item_height = max(
            item.max_height_m for item in self.items if item.max_height_m is not None
        )
        if self.common_scale_max_m is None:
            return
        if not isfinite(self.common_scale_max_m) or self.common_scale_max_m <= 0:
            raise ValueError('Common stockpile scale must be greater than zero')
        if self.common_scale_max_m < maximum_item_height:
            raise ValueError('Common stockpile scale must cover every item maximum height')

    def _validate_fixed_percentage_mode(self) -> None:
        if self.common_scale_max_m is not None:
            raise ValueError('Fixed-percentage stockpiles do not use a height scale')
        if any(item.height_m is not None for item in self.items):
            raise ValueError('Fixed-percentage stockpiles must not contain height values')


@dataclass(frozen=True, slots=True)
class StockpileTheme:
    card_start: str = '#f3f4f5'
    card_end: str = '#e4e6e8'
    text_primary: str = '#3e464f'
    text_secondary: str = '#69717a'
    pile_dark: str = '#515860'
    pile_mid: str = '#a9adb2'
    pile_light: str = '#d5d7da'
    fill_top: str = '#616972'
    fill_bottom: str = '#343a41'
    track: str = '#8c939a'
    badge: str = '#59616a'
    badge_text: str = '#ffffff'


@dataclass(frozen=True, slots=True)
class StockpileRenderOptions:
    show_card: bool = True
    show_title: bool = True
    show_item_maximum: bool = True
    cell_width: int = 230
    gap: int = 18
    height: int = 330

    def __post_init__(self) -> None:
        if self.cell_width < 160:
            raise ValueError('Stockpile cell width must be at least 160 pixels')
        if self.gap < 0:
            raise ValueError('Stockpile gap must be greater than or equal to zero')
        if self.height < 260:
            raise ValueError('Stockpile SVG height must be at least 260 pixels')
