from __future__ import annotations
from io import BytesIO

from wand.exceptions import TypeError
from wand.image import Image
from typing import Callable, Tuple, TYPE_CHECKING

from app.exceptions.errors import BadImage, FileLarge, ManipulationError

if TYPE_CHECKING:
    from typing_extensions import ParamSpec, Concatenate
    P = ParamSpec('P')
else:
    from typing import TypeVar
    P = TypeVar('P')


class WandManip:
    @staticmethod
    def wand_open(byt: bytes) -> Image:
        if byt.__sizeof__() > 10 * (2**20):
            raise FileLarge("Large file")
        try:
            return Image(blob=byt)
        except TypeError:
            raise BadImage("Invalid Format")

    @staticmethod
    def wand_save(byt: bytes) -> BytesIO:
        io = BytesIO(byt)
        io.seek(0)
        return io


def wand_static(
    function: Callable[Concatenate[Image, P], Image]
) -> Callable[P, Tuple[BytesIO, str]]:
    def wrapper(image: bytes, *args: P.args,
                **kwargs: P.kwargs) -> Tuple[BytesIO, str]:
        img = WandManip.wand_open(image)
        if img.format in ["PNG", "JPEG"]:
            dst_image: Image = function(img, *args, **kwargs)
            byt = dst_image.make_blob()
        else:
            raise BadImage("Invalid Format")
        if byt:
            return WandManip.wand_save(byt), img.format
        else:
            raise ManipulationError("No bytes from saving Image")

    return wrapper


def wand(
    function: Callable[Concatenate[Image, P], Image]
) -> Callable[Concatenate[bytes, P], Tuple[BytesIO, str]]:
    def wrapper(image: bytes, *args: P.args,
                **kwargs: P.kwargs) -> Tuple[BytesIO, str]:
        img = WandManip.wand_open(image)
        img_format = ""
        if img.format:
            img_format = img.format
        else:
            raise BadImage("Invalid Format")
        if img_format == "GIF":
            with Image() as dst_image:
                for frame in img.sequence:
                    frame = function(frame, *args, **kwargs)
                    dst_image.sequence.append(frame)
                byt = dst_image.make_blob()
        elif img_format in ["PNG", "JPEG"]:
            dst_image = function(img, *args, **kwargs)
            byt = dst_image.make_blob()
        else:
            raise BadImage("Inavlid Format")
        if byt:
            return WandManip.wand_save(byt), str(img_format)
        else:
            raise ManipulationError("No bytes returned")

    return wrapper
