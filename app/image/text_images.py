from datetime import datetime

from PIL import Image, ImageDraw, ImageFont, ImageOps

from app.image.PILManip import static_pil
from app.image.decorators import executor
from app.image.writetext import WriteText
from app.exceptions.errors import ParameterError


__all__ = ('tweet_gen', 'quote', )


@executor
@static_pil
def tweet_gen(image, username: str, text: str):
    print(len(text))
    if len(text) > 180:
        raise ParameterError('Text supplied is too long')
    today = datetime.today()
    m_list = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "October",
        "November",
        "December",
    ]
    m = today.month
    mo = m_list[int(m - 1)]

    h = today.hour
    if h > 12:
        su = "PM"
        h = h - 12
    else:
        su = "AM"
    y = str(today.day).strip("0")
    t_string = f"{h}:{today.minute} {su} - {y} {mo} {today.year}"
    tweet = Image.open("app/image/assets/tweet.png").convert('RGBA')
    st = username
    lst = st.lower()
    to_pa = image.resize((150, 150), 5)
    size = (100, 100)
    mask = Image.new("L", size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0) + size, fill=255)
    avatar = ImageOps.fit(to_pa, mask.size, centering=(0.5, 0.5))
    tweet.paste(avatar, (20, 20), mask=mask)
    d = ImageDraw.Draw(tweet)
    fntna = ImageFont.truetype("app/image/assets/HelveticaNeue Medium.ttf", 25)
    fnth = ImageFont.truetype("app/image/assets/HelveticaNeue Light.ttf", 25)
    fntt = ImageFont.truetype("app/image/assets/HelveticaNeue Light.ttf", 18)
    d.multiline_text((140, 35), st, font=fntna, fill=(0, 0, 0))
    d.multiline_text((143, 60), f"@{lst}", font=fnth,
                     fill=(101, 119, 134, 178))
    d.multiline_text((30, 320), t_string, font=fntt, fill=(101, 119, 134, 178))
    margin = 30
    offset = 100
    img_wrap = WriteText(tweet)
    img_wrap.write_text_box(
        margin, offset, text, 630, "app/image/assets/HelveticaNeue Medium.ttf",
        30, (0, 0, 0)
    )
    return img_wrap.ret_img()


@executor
@static_pil
def quote(image, username: str, text: str):
    today = datetime.today()
    y = Image.new("RGBA", (2400, 800), (0, 0, 0, 0))
    to_pa = image.resize((150, 150), 5)
    size = (150, 150)
    mask = Image.new("L", size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0) + size, fill=255)
    avatar = ImageOps.fit(to_pa, mask.size, centering=(0.5, 0.5))
    y.paste(avatar, (50, 60), mask=mask)
    h = today.hour
    if h > 12:
        su = "PM"
        h = h - 12
    else:
        su = "AM"
    t_string = f"Today at {h}:{today.minute} {su}"
    d = ImageDraw.Draw(y)
    fntd = ImageFont.truetype("app/image/assets/whitney-medium.ttf", 80)
    fntt = ImageFont.truetype("app/image/assets/whitney-medium.ttf", 40)
    if len(text) > 1000:
        print("text too long")
    else:
        d.text((260, 50), username, color=(256, 256, 256), font=fntd)
        wi = fntd.getsize(username)
        d.text((310 + wi[0], 80), t_string, color=(114, 118, 125), font=fntt)
        wrap = WriteText(y)
        f = wrap.write_text_box(
            260, 80, text, 2120, "app/image/assets/whitney-medium.ttf", 50,
            color=(256, 256, 256)
        )
        print(f)
        im = wrap.ret_img()
        ima = im.crop((0, 0, 2400, (f + 90)))
        top = Image.new("RGBA", ima.size, (0, 0, 0, 0))
        return Image.alpha_composite(top, ima)
