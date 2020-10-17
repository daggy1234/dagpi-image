import functools
from io import BytesIO
from typing import List

from PIL import Image, ImageSequence, UnidentifiedImageError

from app.exceptions.errors import BadImage, FileLarge


class PILManip:
    @staticmethod
    def pil_image(image: bytes) -> Image:
        if image.__sizeof__() > 8 * (2 ** 20):
            raise FileLarge()
        try:
            io = BytesIO(image)
            io.seek(0)
            return Image.open(io)
        except UnidentifiedImageError:
            raise BadImage("Unable to use Image")

    @staticmethod
    def pil_image_save(img: Image) -> BytesIO:
        image_bytes = BytesIO()
        img.save(image_bytes, format="png")
        image_bytes.seek(0)
        return image_bytes

    @staticmethod
    def pil_gif_save(frames: List) -> BytesIO:
        image_bytes = BytesIO()
        frames[0].save(image_bytes, format="gif", save_all=True, append_images=frames)
        image_bytes.seek(0)
        return image_bytes


def pil(function):
    @functools.wraps(function)
    def wrapper(image, *args, **kwargs):
        img = PILManip.pil_image(image)
        if img.format == "GIF":
            frames = []
            for frame in ImageSequence.Iterator(img):
                res_frame = function(frame, *args, **kwargs)
                frames.append(res_frame)
            return PILManip.pil_gif_save(frames), "gif"
        elif img.format == "PNG" or img.format == "JPEG":
            img = function(img, *args, **kwargs)
            return PILManip.pil_image_save(img), "png"

    return wrapper


def double_image(function):
    @functools.wraps(function)
    def wrapper(image_a, image_b, *args, **kwargs):
        image_a = PILManip.pil_image(image_a)
        image_b = PILManip.pil_image(image_b)
        img = function(image_a, image_b, *args, **kwargs)
        return PILManip.pil_image_save(img)

    return wrapper


def static_pil(function):
    @functools.wraps(function)
    def wrapper(image, *args, **kwargs):
        img = PILManip.pil_image(image)
        img = function(img, *args, **kwargs)
        return PILManip.pil_image_save(img)

    return wrapper
