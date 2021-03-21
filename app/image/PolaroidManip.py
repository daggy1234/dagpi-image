
from polaroid import Image

from app.exceptions.errors import BadImage, FileLarge, ManipulationError

import functools
from io import BytesIO


class PolaroidManip:
    @staticmethod
    def polaroid_image(image: bytes) -> Image:
        if image.__sizeof__() > 10 * (2 ** 20):
            raise FileLarge("Exceeds 10MB")
        try:
            return Image(image)
        except Exception as e:
            raise BadImage(str(e))

    @staticmethod
    def polaroid_image_save(image: Image) -> BytesIO:
        try:
            byt = image.save_bytes()
            return BytesIO(byt)
        except Exception:
            raise ManipulationError("Error encoding")


def polaroid(function):
    @functools.wraps(function)
    def wrapper(image, *args, **kwargs) -> BytesIO:
        img = PolaroidManip.polaroid_image(image)
        out = function(img, *args, **kwargs)
        return PolaroidManip.polaroid_image_save(out)
    return wrapper
