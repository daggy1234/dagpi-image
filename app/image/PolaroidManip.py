from __future__ import annotations
from app.exceptions.errors import BadImage, FileLarge, ManipulationError
import polaroid
from typing import TYPE_CHECKING, Callable
from io import BytesIO

if TYPE_CHECKING:
    from typing_extensions import ParamSpec, Concatenate
    P = ParamSpec('P')
else:
    from typing import TypeVar
    P = TypeVar('P')


class PolaroidManip:
    @staticmethod
    def polaroid_image(image: bytes) -> polaroid.Image:
        if image.__sizeof__() > 10 * (2**20):
            raise FileLarge("Exceeds 10MB")
        try:
            return polaroid.Image(image)
        except Exception as e:
            raise BadImage(str(e))

    @staticmethod
    def polaroid_image_save(image: polaroid.Image) -> BytesIO:
        try:
            byt = image.save_bytes()
            return BytesIO(byt)
        except Exception:
            raise ManipulationError("Error encoding")


def polaroid(
    function: Callable[Concatenate[polaroid.Image, P], polaroid.Image]
) -> Callable[Concatenate[bytes, P], BytesIO]:
    def wrapper(image: bytes, *args, **kwargs) -> BytesIO:
        img = PolaroidManip.polaroid_image(image)
        out = function(img, *args, **kwargs)
        return PolaroidManip.polaroid_image_save(out)

    return wrapper
