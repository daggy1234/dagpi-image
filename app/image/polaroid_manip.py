from app.image.decorators import executor
from app.image.PolaroidManip import polaroid as polaroid_deco
import polaroid


__all__ = ("glitch", "comic_manip_static")

@executor
@polaroid_deco
def glitch(img: polaroid.Image) -> polaroid.Image:
    img.offset_red(30)
    return img


@executor
@polaroid_deco
def comic_manip_static(img: polaroid.Image) -> polaroid.Image:
    img.threshold(100)
    return img
