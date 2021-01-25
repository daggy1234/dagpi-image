import functools
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, UnidentifiedImageError

from app.exceptions.errors import BadImage, FileLarge


class NumpyManip:
    @staticmethod
    def image_read(image: bytes) -> np.ndarray:
        if image.__sizeof__() > 10 * (2 ** 20):
            raise FileLarge("Image Exceeds maximum size")
        try:
            io = BytesIO(image)
            io.seek(0)
            im = Image.open(io)
            return np.asarray(im)
        except UnidentifiedImageError:
            raise BadImage("Unable to use Image")

    @staticmethod
    def image_save(arr) -> BytesIO:
        image_bytes = BytesIO()
        plt.imsave(image_bytes, arr)
        image_bytes.seek(0)
        return image_bytes


def numpy(function):
    @functools.wraps(function)
    def wrapper(image, *args, **kwargs):
        img = NumpyManip.image_read(image)
        ret_img = function(img, *args, **kwargs)
        return NumpyManip.image_save(ret_img)

    return wrapper
