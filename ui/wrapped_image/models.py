from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .definitions import OverrideState


@dataclass(frozen=True, slots=True)
class WrappedImageModel:
    label: str | None = None
    label_font_size: str | None  = None
    label_position: str = ''
    image: str | None = None
    variant: str | None = None
    override_state: OverrideState = OverrideState()

    def to_component(self):
        from .build import build_wrapped_image
        return build_wrapped_image(model=self)

@dataclass(frozen=True, slots=True)
class WrappedImageGroupModel:
    images_orientation: str
    images: tuple[WrappedImageModel, ...] = tuple()

    @classmethod
    def from_iterable(
        cls,
        images: Iterable[WrappedImageModel],
        images_orientation: str,
    ) -> WrappedImageGroupModel:
        return cls(
            images_orientation=images_orientation,
            images=tuple(images)
        )

    def to_component(self):
        from .build import build_wrapped_images_group
        return build_wrapped_images_group(models=self)

    def __iter__(self) -> Iterable[WrappedImageModel]:
        return iter(self.images)

    def __len__(self) -> int:
        return len(self.images)