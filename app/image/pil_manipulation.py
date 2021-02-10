import random
from io import BytesIO

import numpy as np
from PIL import Image
from PIL import Image as PILImage
from PIL import (ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps,
                 ImageSequence, ImageChops)

from app.exceptions.errors import ParameterError
from app.image.PILManip import PILManip, double_image, pil, static_pil
from app.image.decorators import executor
from app.image.writetext import WriteText

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
    "memegen",
    "america",
    "communism",
    "pride",
    "delete",
    "shatter",
    "fedora",
    "stringify",
    "mosiac",
    "neon_static"
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
    img = img.resize((int(width ** 0.75), int(height ** 0.75)),
                     resample=Image.LANCZOS)
    img = img.resize((int(width ** 0.88), int(height ** 0.88)),
                     resample=Image.BILINEAR)
    img = img.resize((int(width ** 0.9), int(height ** 0.9)),
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
def pride(image, flag: str):
    try:
        im = Image.open(f"app/image/assets/pride/{flag}.png").convert(
            "RGBA").resize((300, 300))
    except FileNotFoundError:
        raise ParameterError(f"Invalid Pride Filter {flag}")
    ima = image.resize((300, 300)).convert("RGBA")
    im.putalpha(175)
    ima.paste(im, (0, 0), mask=im)
    return ima


@executor
@pil
def shatter(image):
    im = Image.open("app/image/assets/glass.png").convert(
        "RGBA").resize((300, 300))
    ima = image.resize((300, 300)).convert("RGBA")
    ima.paste(im, (0, 0), mask=im)
    return ima


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
        r" .'`^\,:;Il!i><~+_-?][}{1)(|\/tfjrxn"
        r"uvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
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
    img = (1.0 - img / img.max()) ** gcf * (chars.size - 1)
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
def delete(img):
    im = Image.open("app/image/assets/delete.BMP").convert("RGBA")
    ima = img.resize((195, 195)).convert("RGBA")
    im.paste(ima, (120, 135), ima)
    return im


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
    fim = im.resize((width, height), 5)
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
def fedora(image):
    img = Image.open('app/image/assets/fedora.bmp').convert('RGBA')
    av = image.resize((275, 275)).convert('RGBA')
    final = Image.new('RGBA', img.size)
    final.paste(av, (112, 101), av)
    final.paste(img, (0, 0), img)
    return final


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


@executor
@static_pil
def stringify(im):
    im = im.convert("L")
    im.thumbnail((50, 50))
    brightest = int(
        (sorted(np.array(im).flatten(), reverse=True)[0] / 255) * 100)
    width, height = im.size
    canvas = Image.new("L", (width * 100 - 100, height * 100))
    arr = np.flipud(np.rot90(np.array(im)))
    draw = ImageDraw.Draw(canvas)

    every_first = arr[::1, ::1]
    every_second = arr[1::1, ::1]

    for row_index, (row1, row2) in enumerate(zip(every_first, every_second)):
        for column_index, (color1, color2) in enumerate(zip(row1, row2)):
            height1 = 2 * ((int((color1 / 255) * 100) * 100) / brightest)
            height2 = 2 * ((int((color2 / 255) * 100) * 100) / brightest)

            draw.polygon(
                (
                    (row_index * 100, column_index * 100 + 100),
                    (row_index * 100, column_index * 100 + height1),
                    (row_index * 100 + 100, column_index * 100 + height2),
                    (row_index * 100 + 100, column_index * 100 + 100)
                ),
                fill="black")

            for offset in range(3):
                draw.line(
                    (
                        (row_index * 100, column_index *
                         100 + height1 + offset * 3),
                        (row_index * 100 + 100, column_index *
                         100 + height2 + offset * 3)
                    ),
                    fill="white", width=12, joint="curve")
    return canvas


@executor
@pil
def mosiac(img, pixels: int = None):
    """
    Heavily Inspired by the code used by
    https://github.com/TrustyJAID/Trusty-cogs/blob/a236336034c981d8ea25155ef0c8f3f9d3fc4132/notsobot/notsobot.py#L1238-L1262
    """
    print(img.size)
    img = img.convert("RGBA").resize(
        (int(img.size[0] / pixels), int(img.size[1] / pixels)), 5).resize(
        (int(img.size[0] * pixels), int(img.size[1] * pixels)), 5)
    bg = (0, 0, 0)
    width, height = img.size
    load = img.load()
    for i in range(0, width, pixels):
        for j in range(0, height, pixels):
            for r in range(pixels):
                load[i + r, j] = bg
                load[i, j + r] = bg
    return img


@executor
@pil
def memegen(tv, text: str):
    wid = tv.size[0]
    hei = tv.size[0]
    if 0 < wid < 200:
        sfm = [25, 15, 10, 5]
        mplier = 0.1
        hply = 0.1
    elif 400 > wid >= 200:
        sfm = [30, 20, 10, 5]
        mplier = 0.075
        hply = 0.2
    elif 400 <= wid < 600:
        sfm = [50, 30, 20, 10]
        mplier = 0.05
        hply = 0.3
    elif 800 > wid >= 600:
        sfm = [70, 50, 30, 20]
        mplier = 0.025
        hply = 0.4
    elif 1000 > wid >= 800:
        sfm = [80, 60, 40, 30]
        mplier = 0.01
        hply = 0.5
    elif 1500 > wid >= 1000:
        sfm = [100, 80, 60, 40]
        mplier = 0.01
        hply = 0.6
    elif 2000 > wid >= 1400:
        sfm = [120, 100, 80, 60]
        mplier = 0.01
        hply = 0.6
    elif 2000 <= wid < 3000:
        sfm = [140, 120, 100, 80]
        mplier = 0.01
        hply = 0.6
    elif wid >= 3000:
        sfm = [180, 160, 140, 120]
        mplier = 0.01
        hply = 0.6
    else:
        raise ParameterError("Image is too large")
    x_pos = int(mplier * wid)
    y_pos = int(-1 * (mplier * hply * 10) * hei)
    print(y_pos)
    if 50 > len(text) > 0:
        size = sfm[1]
    elif 100 > len(text) > 50:
        size = sfm[1]
    elif 100 < len(text) < 250:
        size = sfm[2]
    elif len(text) > 250 and len(text) > 500:
        size = sfm[3]
    elif 500 < len(text) < 1000:
        size = sfm[4]
    else:
        raise ParameterError("text is too long")
    y = Image.new("RGBA", (tv.size[0], 800), (256, 256, 256))
    wra = WriteText(y)
    f = wra.write_text_box(
        x_pos, -10, text, tv.size[0] - 40,
        "app/image/assets/whitney-medium.ttf",
        size, color=(0, 0, 0)
    )
    t = f
    im = wra.ret_img()
    # im = Image.open(bt)
    ima = im.crop((0, 0, tv.size[0], t))
    bcan = Image.new("RGBA", (tv.size[0], tv.size[1] + t), (0, 0, 0, 0))
    bcan.paste(ima)
    bcan.paste(tv, (0, t))
    return bcan


@executor
def america(byt: bytes) -> BytesIO:
    img = PILManip.static_pil_image(byt)
    image = img.convert("RGBA").resize((480, 480), 5)
    flag = Image.open("app/image/assets/america.gif")
    image.putalpha(96)
    frame_list = list()
    for frame in ImageSequence.Iterator(flag):
        frame = frame.resize((480, 480), 5).convert("RGBA")
        frame.paste(image, (0, 0), image)
        frame_list.append(frame)
    obj = BytesIO()
    frame_list[0].save(obj, format='gif', save_all=True,
                       append_images=frame_list[1:], loop=0, disposal=2,
                       optimize=True)
    obj.seek(0)
    return obj


@executor
def communism(byt: bytes) -> BytesIO:
    img = PILManip.static_pil_image(byt)
    image = img.convert("RGBA").resize((480, 480), 5)
    flag = Image.open("app/image/assets/communism.gif")
    image.putalpha(96)
    frame_list = list()
    for frame in ImageSequence.Iterator(flag):
        frame = frame.resize((480, 480), 5).convert("RGBA")
        frame.paste(image, (0, 0), image)
        frame_list.append(frame)
    obj = BytesIO()
    frame_list[0].save(obj, format='gif', save_all=True,
                       append_images=frame_list, loop=0, disposal=2,
                       optimize=True)
    obj.seek(0)
    return obj


def preprocess_neon(im, *, single, **kwargs):
    sharpen = kwargs.get('sharpen', None)
    saturation = kwargs.get('saturation', None)
    overlay = kwargs.get('overlay', False)
    im = im.convert('RGBA')
    maxsize = kwargs.get('maxsize', 512 if single else 256)
    size = max(im.size)
    if size > maxsize:
        ratio = size / maxsize
        im = im.resize((int(im.width / ratio), int(im.height / ratio)))
    else:
        im = im
    if sharpen is not None:
        filters = (ImageFilter.SHARPEN, ImageFilter.EDGE_ENHANCE,
                   ImageFilter.EDGE_ENHANCE_MORE)
        try:
            im = im.filter(filters[sharpen])
        except IndexError:
            pass
    if overlay:
        enhance = ImageEnhance.Brightness(im)
        im = enhance.enhance(0.85)
    if saturation is not None:
        enhancer = ImageEnhance.Color(im)

        im = enhancer.enhance(saturation)

    return im


def create_soft_outline(outline, single, multi):
    soft = outline.filter(ImageFilter.GaussianBlur(10))
    enhancer = ImageEnhance.Brightness(soft)
    soft = enhancer.enhance(1.9 if single and not multi else 1.5)
    return soft


def create_sharp_outline(im, single, multi):
    countour_outline = ImageChops.invert(
        im.filter(ImageFilter.CONTOUR).convert('L'))
    enhancer = ImageEnhance.Brightness(countour_outline)
    countour_outline = enhancer.enhance(3.0 if single and not multi else 2.0)
    width, height = countour_outline.size
    width -= 1
    height -= 1
    draw = ImageDraw.Draw(countour_outline)
    draw.line((0, 0, 0, height), 0, 1)
    draw.line((0, 0, width, 0), 0, 1)
    draw.line((width, height, 0, height), 0, 1)
    draw.line((width, height, width, 0), 0, 1)
    return countour_outline


def color_range(start, end, steps):
    delta = tuple((cur - nc) / steps for cur, nc in zip(start, end))
    for i in range(steps):
        yield tuple(cur - int(d * i) for cur, d in zip(start, delta))


def neon_static_breathing(im, mask, colors, single, *, overlay,
                          per_color) -> list:
    if single:
        with Image.new('RGB', im.size, colors) as paste:
            temp = im if overlay else Image.new('RGBA', im.size, (0, 0, 0, 0))
            temp.paste(paste, mask=mask)
        return [temp]
    else:
        frames = []
        iter_colors = iter(colors + type(colors)((colors[0],)))
        next_color = next(iter_colors)
        while True:
            try:
                current = next_color
                next_color = next(iter_colors)
            except StopIteration:
                break
            for color in color_range(current, next_color, per_color):
                with Image.new('RGB', im.size, color) as paste:
                    temp = im.copy() if overlay else Image.new('RGBA', im.size,
                                                               (0, 0, 0, 0))
                    temp.paste(paste, mask=mask)
                frames.append(temp)
        return frames


@executor
def neon_static(byt, sharp, soft, overlay, gradient, multi, per_color, colors,
                **kwargs) -> BytesIO:
    image = PILManip.static_pil_image(byt)
    if not (sharp or soft):
        raise ParameterError("both sharp and soft can't be false")
    if all(isinstance(c, (tuple, list)) for c in colors):
        if len(colors) == 1:
            single = True
            colors = tuple(colors[0])
        else:
            if gradient in (0, 1, 2):
                single = gradient == 1
            else:
                raise ParameterError('gradient must be between 0 <= x <= 2')
    elif all(isinstance(c, int) for c in colors) and len(colors) == 3:
        single = True
    else:
        raise ParameterError(
            'colors must be a tuple/list of RGB tuples or RGB tuple')
    im = preprocess_neon(image, single=single, **kwargs)
    outline = create_sharp_outline(im, single, multi)
    with Image.new('RGBA', im.size, (0, 0, 0, 0)) as mask:
        if soft:
            with create_soft_outline(outline, single, multi) as soft:
                mask.paste(soft, mask=soft)
        if sharp:
            mask.paste(outline, mask=outline)
            outline.close()
        frame_list = neon_static_breathing(im, mask, colors, single,

                                           overlay=overlay,

                                           per_color=per_color)
    obj = BytesIO()
    frame_list[0].save(obj, format='gif', save_all=True,
                       append_images=frame_list, loop=0,
                       optimize=True)
    obj.seek(0)
    return obj
