from __future__ import annotations

from dataclasses import dataclass
from ..wrapped_image.models import WrappedImageModel

@dataclass(frozen=True, slots=True)
class PointCardModel:
    image: WrappedImageModel

    @classmethod
    def from_image(cls, image: WrappedImageModel) -> PointCardModel:
        return cls(image=image)

    def to_component(self) -> PointCardModel:
        from .build import build_point
        return build_point(model=self.image)

@dataclass(frozen=True, slots=True)
class PointCardGroupModel:
    images: tuple[WrappedImageModel, ...]

    @classmethod
    def from_images(cls, images: tuple[WrappedImageModel, ...]) -> PointCardModel:
        return cls(images=images)

    def to_component(self):
        from .build import build_points
        return build_points(models=self.images)

    def __len__(self) -> int:
        return len(self.images)