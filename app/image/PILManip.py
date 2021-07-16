from __future__ import annotations
import functools
from typing import List, Tuple, TYPE_CHECKING, Callable
from app.executor import get_executor
import asyncio

if TYPE_CHECKING:
    from typing_extensions import ParamSpec, Concatenate
    P = ParamSpec('P')
else:
    from typing import TypeVar
    P = TypeVar('P')

from io import BytesIO

from PIL import Image, ImageSequence, UnidentifiedImageError

from app.exceptions.errors import BadImage, FileLarge


class PILManip:
    @staticmethod
    def pil_image(image: bytes) -> Image.Image:
        if image.__sizeof__() > 10 * (2**20):
            raise FileLarge("Exceeds 10MB")
        try:
            io = BytesIO(image)
            io.seek(0)
            return Image.open(io, formats=["PNG", "JPEG", "GIF"])
        except UnidentifiedImageError:
            raise BadImage("Unable to use Image")

    @staticmethod
    def static_pil_image(image: bytes) -> Image.Image:
        if image.__sizeof__() > 15 * (2**20):
            raise FileLarge("File Exceeds 15 Mb")
        try:
            io = BytesIO(image)
            io.seek(0)
            return Image.open(io, formats=["PNG", "JPEG", "GIF"])
        except UnidentifiedImageError as e:
            print(e)
            raise BadImage("Unable to use Image")

    @staticmethod
    def pil_image_save(img: Image.Image) -> BytesIO:
        image_bytes = BytesIO()
        img.save(image_bytes, format="png")
        image_bytes.seek(0)
        return image_bytes

    @staticmethod
    def pil_gif_save(frames: List[Image.Image]) -> BytesIO:
        image_bytes = BytesIO()
        frames[0].save(image_bytes,
                       format="gif",
                       save_all=True,
                       loop=0,
                       append_images=frames)
        image_bytes.seek(0)
        return image_bytes


def pil_manip_static(image: bytes, function: Callable[Concatenate[Image.Image,
                                                                  P],
                                                      Image.Image], *args,
                     **kwargs) -> BytesIO:
    img = PILManip.static_pil_image(image)
    img = function(img, *args, **kwargs)
    return PILManip.pil_image_save(img)


def pil_manip(image: bytes, function: Callable[Concatenate[Image.Image, P],
                                               Image.Image], *args,
              **kwargs) -> Tuple[BytesIO, str]:
    img = PILManip.pil_image(image)
    if img.format == "GIF":
        frames = []
        for frame in ImageSequence.Iterator(img):
            res_frame = function(frame, *args, **kwargs)
            frames.append(res_frame)
        return PILManip.pil_gif_save(frames), "gif"
    elif img.format in ["PNG", "JPEG"]:
        img = function(img, *args, **kwargs)
        return PILManip.pil_image_save(img), "png"
    else:
        raise BadImage("Bad Format")


async def pil(function: Callable[Concatenate[Image.Image, P], Image.Image],
              byt: bytes, *args, **kwargs) -> Tuple[BytesIO, str]:
    loop = asyncio.get_event_loop()
    fn = functools.partial(pil_manip, byt, function, *args, **kwargs)
    out = await loop.run_in_executor(get_executor(), fn)
    return out


async def static_pil(function: Callable[Concatenate[Image.Image, P],
                                        Image.Image], byt: bytes, *args,
                     **kwargs) -> BytesIO:
    loop = asyncio.get_event_loop()
    fn = functools.partial(pil_manip_static, byt, function, *args, **kwargs)
    out = await loop.run_in_executor(get_executor(), fn)
    return out


def double_image_manip(function: Callable[Concatenate[Image.Image, Image.Image,
                                                      P], Image.Image],
                       image_a: bytes, image_b: bytes, *args: P.args,
                       **kwargs: P.kwargs) -> BytesIO:
    p_image_a = PILManip.static_pil_image(image_a)
    p_image_b = PILManip.static_pil_image(image_b)
    img = function(p_image_a, p_image_b, *args, **kwargs)
    return PILManip.pil_image_save(img)


async def pil_multi_image(function: Callable[Concatenate[Image.Image,
                                                         Image.Image, P],
                                             Image.Image], image: bytes,
                          image_2: bytes, *args, **kwargs) -> BytesIO:
    loop = asyncio.get_event_loop()
    fn = functools.partial(double_image_manip, function, image, image_2, *args,
                           **kwargs)
    out = await loop.run_in_executor(get_executor(), fn)
    return out


# def pil(
#     function: Callable[Concatenate[Image.Image, P], Image.Image]
# ) -> Callable[Concatenate[bytes, P], Tuple[BytesIO, str]]:
#     def wrapper(image: bytes, *args, **kwargs) -> Tuple[BytesIO, str]:
#         img = PILManip.pil_image(image)
#         if img.format == "GIF":
#             frames = []
#             for frame in ImageSequence.Iterator(img):
#                 res_frame = function(frame, *args, **kwargs)
#                 frames.append(res_frame)
#             return PILManip.pil_gif_save(frames), "gif"
#         elif img.format in ["PNG", "JPEG"]:
#             img = function(img, *args, **kwargs)
#             return PILManip.pil_image_save(img), "png"
#         else:
#             raise BadImage("Bad Format")

#     return wrapper
