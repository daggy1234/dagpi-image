from io import BytesIO
import os
from PIL import Image
from app.image.PILManip import PILManip
from app.image.decorators import executor

__all__ = (
    "special",
)

@executor
def special(byt: bytes) -> BytesIO:
    img = PILManip.static_pil_image(byt)
    image = img.resize((300, 300)).convert("RGBA")
    frame_list = []
    flags = os.listdir("app/image/assets/pride")
    for flag in flags:
        im = Image.open(f"app/image/assets/pride/{flag}").convert(
            "RGBA").resize((300, 300))
        im.putalpha(96)
        copies = image.copy()
        copies.paste(im, (0, 0), mask=im)
        frame_list.append(copies)
    obj = BytesIO()
    frame_list[0].save(obj, format='gif', save_all=True,
                       duration=500,
                       append_images=frame_list[1:], loop=0, disposal=2,
                       optimize=True)
    obj.seek(0)
    return obj