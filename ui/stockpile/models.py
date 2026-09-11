from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class StockpileMode(StrEnum):
    MINE = "mine"
    FIXED = "fixed"


@dataclass(frozen=True, slots=True)
class StockpileItem:
    key: str
    label: str
    percent: float
    height_m: float | None = None
    max_height_m: float | None = None

    def __post_init__(self) -> None:
        if not self.key.strip():
            raise ValueError("Stockpile key cannot be empty")
        if not self.label.strip():
            raise ValueError("Stockpile label cannot be empty")
        if not 0 <= self.percent <= 100:
            raise ValueError("Stockpile percent must be between 0 and 100")
        if self.height_m is not None and self.height_m < 0:
            raise ValueError("Stockpile height cannot be negative")
        if self.max_height_m is not None and self.max_height_m <= 0:
            raise ValueError("Stockpile maximum height must be greater than zero")
        if (
            self.height_m is not None
            and self.max_height_m is not None
            and self.height_m > self.max_height_m
        ):
            raise ValueError("Stockpile height cannot exceed its maximum height")


@dataclass(frozen=True, slots=True)
class StockpilePanel:
    title: str
    mode: StockpileMode
    items: tuple[StockpileItem, ...]
    common_scale_m: float = 30.0

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("Stockpile panel title cannot be empty")
        if not self.items:
            raise ValueError("Stockpile panel must contain at least one item")

        keys = [item.key for item in self.items]
        if len(keys) != len(set(keys)):
            raise ValueError("Stockpile item keys must be unique")

        if self.mode is StockpileMode.MINE:
            if self.common_scale_m <= 0:
                raise ValueError("Common scale must be greater than zero")
            for item in self.items:
                if item.height_m is None or item.max_height_m is None:
                    raise ValueError("Mine stockpiles require height and maximum height")
                if item.max_height_m > self.common_scale_m:
                    raise ValueError("Stockpile maximum height cannot exceed the common scale")
        else:
            for item in self.items:
                if item.height_m is not None or item.max_height_m is not None:
                    raise ValueError("Fixed stockpiles cannot define height values")
