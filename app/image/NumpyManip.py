from __future__ import annotations
from io import BytesIO
import functools
import asyncio
from app.executor import get_executor
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from typing_extensions import ParamSpec, Concatenate
    P = ParamSpec('P')
else:
    from typing import TypeVar
    P = TypeVar('P')

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, UnidentifiedImageError

from app.exceptions.errors import BadImage, FileLarge


class NumpyManip:
    @staticmethod
    def image_read(image: bytes) -> np.ndarray:
        if image.__sizeof__() > 10 * (2**20):
            raise FileLarge("Image Exceeds maximum size")
        try:
            io = BytesIO(image)
            io.seek(0)
            im = Image.open(io)
            return np.asarray(im)
        except UnidentifiedImageError:
            raise BadImage("Unable to use Image")

    @staticmethod
    def image_save(arr: np.ndarray) -> BytesIO:
        image_bytes = BytesIO()
        plt.imsave(image_bytes, arr)
        image_bytes.seek(0)
        return image_bytes


def numpy_manip(
    image: bytes,
    function: Callable[Concatenate[np.ndarray, P], np.ndarray],
    *args,
    **kwargs
) -> BytesIO:
    img = NumpyManip.image_read(image)
    ret_img = function(img, *args, **kwargs)
    return NumpyManip.image_save(ret_img)

async def numpy(function: Callable[Concatenate[np.ndarray, P], np.ndarray], byt: bytes, *args, **kwargs) -> BytesIO:
    loop = asyncio.get_event_loop()
    fn = functools.partial(numpy_manip, byt, function,*args, **kwargs)
    out = await loop.run_in_executor(get_executor(), fn)
    return out