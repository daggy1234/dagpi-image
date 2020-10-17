import random

import numpy as np
from PIL import Image
from PIL import Image as PILImage
from PIL import ImageDraw
from PIL import ImageEnhance
from PIL import ImageFilter
from PIL import ImageFont
from PIL import ImageOps

from app.exceptions.errors import ParameterError
from app.image.decorators import executor
from app.image.PILManip import double_image
from app.image.PILManip import pil
from app.image.PILManip import PILManip
from app.image.PILManip import static_pil

__all__ = (
    "angel",
    "ascii_image",
    "bad_img",
    "blur",
    "deepfry",
    "five_guys_one_girl",
    "gay",
    "htiler",
    "invert",
    "jail",
    "obama",
    "pixelate",
    "satan",
    "sithlord",
    "thought_image",
    "top5colors",
    "trash",
    "triggered",
    "wanted",
    "wasted",
    "why_are_you_gay",
)


@executor
@pil
def test(image: PILImage):
    rim = image.rotate(90)
    print("Rotate")
    return rim


@executor
@pil
def pixelate(image):
    img_small = image.resize((32, 32), resample=Image.BILINEAR)
    return img_small.resize(image.size, Image.NEAREST)


@executor
@pil
def thought_image(image, file: str):
    im = Image.open("app/image/assets/speech.jpg")
    if len(file) > 200:
        raise ParameterError(
            f"Your text is too long {len(file)} is greater than 200")
    else:
        if len(file) > 151:
            fo = file[:50] + "\n" + file[50:]
            ft = fo[:100] + "\n" + fo[100:]
            ff = ft[:150] + "\n" + ft[150:]
            size = 10
        elif len(file) > 101:
            fo = file[:50] + "\n" + file[50:]
            ff = fo[:100] + "\n" + fo[100:]
            size = 12
        elif 51 < len(file) < 100:
            ff = file[:50] + "\n" + file[50:]
            size = 14
        elif 20 < len(file) <= 50:
            ff = file
            size = 18
        else:
            ff = file
            size = 25
        pfp = image.resize((200, 225), 5)
        width = 800
        height = 600
        fim = im.resize((width, height), 4)
        area = (125, 50)
        fim.paste(pfp, area)
        base = fim.convert("RGBA")
        txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
        fnt = ImageFont.truetype("app/image/assets/Helvetica-Bold-Font.ttf",
                                 size)
        d = ImageDraw.Draw(txt)
        d.text((400, 150), f"{ff}", font=fnt, fill=(0, 0, 0, 255))
        return Image.alpha_composite(base, txt)


@executor
@pil
def deepfry(image):
    colours = ((254, 0, 2), (255, 255, 15))
    img = image.convert("RGB")
    width, height = img.width, img.height
    img = img.resize((int(width**0.75), int(height**0.75)),
                     resample=Image.LANCZOS)
    img = img.resize((int(width**0.88), int(height**0.88)),
                     resample=Image.BILINEAR)
    img = img.resize((int(width**0.9), int(height**0.9)),
                     resample=Image.BICUBIC)
    img = img.resize((width, height), resample=Image.BICUBIC)
    img = ImageOps.posterize(img, 4)
    r = img.split()[0]
    r = ImageEnhance.Contrast(r).enhance(2.0)
    r = ImageEnhance.Brightness(r).enhance(1.5)

    r = ImageOps.colorize(r, colours[0], colours[1])

    # Overlay red and yellow onto main image and sharpen the hell out of it
    img = Image.blend(img, r, 0.75)
    return ImageEnhance.Sharpness(img).enhance(100.0)


@executor
@pil
def invert(image):
    frame = image.convert("RGB")
    return ImageOps.invert(frame)


@executor
@pil
def blur(image):
    frame = image.convert("RGBA")
    return frame.filter(ImageFilter.BLUR)


@executor
@pil
def htiler(image):
    im = Image.open("app/image/assets/hitler.jpg")
    pfp = image.resize((260, 300), 5)
    width = 800
    height = 600
    fim = im.resize((width, height), 4)
    area = (65, 40)
    fim.paste(pfp, area)
    return fim


@executor
@pil
def jail(image):
    w, h = image.size
    fil = Image.open("app/image/assets/jail.png")
    filled = fil.resize((w, h), 5)
    ci = image.convert("RGBA")
    ci.paste(filled, mask=filled)
    return ci


@executor
@pil
def gay(image):
    w, h = image.size
    fil = Image.open("app/image/assets/gayfilter.png")
    filled = fil.resize((w, h), 5)
    ci = image.convert("RGBA")
    ci.paste(filled, mask=filled)
    return ci


@executor
@pil
def wasted(image):
    w, h = image.size
    fil = Image.open("app/image/assets/wasted.png")
    fil_r = fil.resize((w, h), 5)
    conv_im = image.convert("RGBA")
    conv_im.paste(fil_r, mask=fil_r)
    return conv_im


@executor
def triggered(byt: bytes):
    im = PILManip.pil_image(byt)
    im = im.resize((500, 500), 1)
    overlay = Image.open("app/image/assets/triggered.png")
    ml = []
    for i in range(0, 30):
        blank = Image.new("RGBA", (400, 400))
        x = -1 * (random.randint(50, 100))
        y = -1 * (random.randint(50, 100))
        blank.paste(im, (x, y))
        rm = Image.new("RGBA", (400, 400), color=(255, 0, 0, 80))
        blank.paste(rm, mask=rm)
        blank.paste(overlay, mask=overlay)
        ml.append(blank)
    return PILManip.pil_gif_save(ml)


@executor
@double_image
def five_guys_one_girl(im, im2):
    back = Image.open("app/image/assets/5g1g.png")
    im = im.resize((150, 150), 1)
    back.paste(im, (80, 100))
    back.paste(im, (320, 10))
    back.paste(im, (575, 60))
    back.paste(im, (830, 60))
    back.paste(im, (1050, 0))
    im2 = im2.resize((150, 150), 1)
    back.paste(im2, (650, 320))
    return back


@executor
@double_image
def why_are_you_gay(gay_image, av_image):
    im = Image.open("app/image/assets/whyareyougay.png")
    mp = av_image.resize((150, 150), 0)
    op = gay_image.resize((150, 150), 0)
    im.paste(op, (550, 100))
    im.paste(mp, (100, 125))
    return im


@executor
@static_pil
def top5colors(image):
    def rgb_to_hex(rgb):
        return ("#%02x%02x%02x" % rgb).upper()

    w, h = image.size
    font = ImageFont.truetype("app/image/assets/Helvetica Neu Bold.ttf",
                              size=30)
    im = image.resize((int(w * (256 / h)), 256), 1)
    q = im.quantize(colors=5, method=2)
    pal = q.getpalette()
    back = Image.new("RGBA", (int(w * (256 / h)) + 200, 256),
                     color=(0, 0, 0, 0))
    d = ImageDraw.Draw(back)
    d.rectangle([10, 10, 40, 40], fill=(pal[0], pal[1], pal[2]))
    d.text((50, 10), rgb_to_hex((pal[0], pal[1], pal[2])), font=font)
    d.rectangle([10, 60, 40, 90], fill=(pal[3], pal[4], pal[5]))
    d.text((50, 60), rgb_to_hex((pal[3], pal[4], pal[5])), font=font)
    d.rectangle([10, 110, 40, 140], fill=(pal[6], pal[7], pal[8]))
    d.text((50, 110), rgb_to_hex((pal[6], pal[7], pal[8])), font=font)
    d.rectangle([10, 160, 40, 190], fill=(pal[9], pal[10], pal[11]))
    d.text((50, 160), rgb_to_hex((pal[9], pal[10], pal[11])), font=font)
    d.rectangle([10, 210, 40, 240], fill=(pal[12], pal[13], pal[14]))
    d.text((50, 210), rgb_to_hex((pal[12], pal[13], pal[14])), font=font)
    back.paste(im, (200, 0))
    return back


# noinspection PyArgumentList
@executor
@static_pil
def ascii_image(image):
    sc = 0.1
    gcf = 2
    bgcolor = (13, 2, 8)
    re_list = list(
        " .'`^\,:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    )
    chars = np.asarray(re_list)
    font = ImageFont.load_default()
    letter_width = font.getsize("x")[0]
    letter_height = font.getsize("x")[1]
    wcf = letter_height / letter_width
    img = image.convert("RGB")

    width_by_letter = round(img.size[0] * sc * wcf)
    height_by_letter = round(img.size[1] * sc)
    s = (width_by_letter, height_by_letter)
    img = img.resize(s)
    img = np.sum(np.asarray(img), axis=2)
    img -= img.min()
    img = (1.0 - img / img.max())**gcf * (chars.size - 1)
    lines = ("\n".join(
        ("".join(r) for r in chars[img.astype(int)]))).split("\n")
    new_img_width = letter_width * width_by_letter
    new_img_height = letter_height * height_by_letter
    new_img = Image.new("RGBA", (new_img_width, new_img_height), bgcolor)
    draw = ImageDraw.Draw(new_img)
    y = 0
    line_idx = 0
    for line in lines:
        line_idx += 1
        draw.text((0, y), line, (0, 255, 65), font=font)
        y += letter_height
    return new_img


@executor
@pil
def satan(image):
    im = Image.open("app/image/assets/satan.jpg")
    base = image.resize((400, 225), 5)
    width = 800
    height = 600
    fim = im.resize((width, height), 4)
    area = (250, 100)
    fim.paste(base, area)
    return fim


@executor
@pil
def wanted(image):
    im = Image.open("app/image/assets/wanted.png")
    tp = image.resize((800, 800), 0)
    im.paste(tp, (200, 450))
    return im


@executor
@pil
def obama(image):
    obama_pic = Image.open("app/image/assets/obama.png")
    y = image.resize((300, 300), 1)
    obama_pic.paste(y, (250, 100))
    obama_pic.paste(y, (650, 0))
    return obama_pic


@executor
@pil
def sithlord(image):
    im = Image.open("app/image/assets/sithlord.jpg")
    to_pa = image.resize((250, 275), 5)
    size = (225, 225)
    mask = Image.new("L", size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((50, 10) + size, fill=255)
    to_pt = ImageOps.fit(to_pa, mask.size, centering=(0.5, 0.5))
    im.paste(to_pt, (225, 180), mask=mask)
    return im


@executor
@pil
def trash(image):
    im = Image.open("app/image/assets/trash.jpg")
    wthf = image.resize((200, 150), 5)
    width = 800
    height = 600
    fim = im.resize((width, height), 4)
    area = (500, 250)
    fim.paste(wthf, area)
    return fim


@executor
@pil
def bad_img(image) -> Image:
    back = Image.open("app/image/assets/bad.png")
    t = image.resize((200, 200), 5)
    back.paste(t, (20, 150))
    return back


@executor
@pil
def angel(image):
    im = Image.open("app/image/assets/angel.jpg")
    base = image.resize((300, 175), 5)
    width = 800
    height = 600
    fim = im.resize((width, height), 4)
    area = (250, 130)
    fim.paste(base, area)
    return fim
