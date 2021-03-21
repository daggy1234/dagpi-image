from app.image.decorators import executor
from app.image.PolaroidManip import polaroid
from polaroid import Image

__all__ = (
    "glitch",
    "comic_manip_static"
)


@executor
@polaroid
def glitch(img: Image) -> Image:
    img.offset_red(30)
    return img


@executor
@polaroid
def comic_manip_static(img: Image) -> Image:
    img.threshold(100)
    return img
