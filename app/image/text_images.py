from datetime import datetime

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps

from app.exceptions.errors import ParameterError
from app.image.PILManip import static_pil
from app.image.decorators import executor
from app.image.writetext import WriteText

__all__ = (
    "tweet_gen",
    "quote",
    "motiv"
)


@executor
@static_pil
def tweet_gen(image, username: str, text: str):
    print(len(text))
    if len(text) > 180:
        raise ParameterError("Text supplied is too long")
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
    tweet = Image.open("app/image/assets/tweet.png").convert("RGBA")
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
    d.multiline_text((143, 60),
                     f"@{lst}",
                     font=fnth,
                     fill=(101, 119, 134, 178))
    d.multiline_text((30, 320), t_string, font=fntt, fill=(101, 119, 134, 178))
    margin = 30
    offset = 100
    img_wrap = WriteText(tweet)
    img_wrap.write_text_box(
        margin,
        offset,
        text,
        630,
        "app/image/assets/HelveticaNeue Medium.ttf",
        30,
        (0, 0, 0),
    )
    return img_wrap.ret_img()


@executor
@static_pil
def motiv(img, top_text: str, bottom_text: str):
    im = img.convert("RGBA")
    new_h, new_w = im.height + im.height * 100, im.width + 200
    white_bg = Image.new("RGBA",(im.width + 10,im.height + 10),(255,255,255))
    base = Image.new("RGBA",(new_w,new_h),(0,0,0))
    white_bg.paste(im, (5,5), im)
    base.paste(white_bg,(100,100),white_bg)
    wt = WriteText(base)
    pos = im.height + 100 + im.height/100
    text_h = wt.write_text_box(100,pos,top_text, im.width, "app/image/assets/times-new-roman.ttf", im.height//5, (255,255,255), place="center", justify_last_line=True)
    text_h_t = wt.write_text_box(100,text_h,bottom_text, im.width, "app/image/assets/times-new-roman.ttf", (2*(im.height//10))//3, (255,255,255), place="center", justify_last_line=True)
    ret = wt.ret_img()
    return ret.crop((0, 0,new_w,text_h_t + 30))


@executor
@static_pil
def quote(image, username: str, text: str, dark: bool):
    today = datetime.today()
    bg = (54,57,63) if dark else (256,256,256)  
    y = Image.new("RGBA", (2400, 800),bg)
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
    fntd = ImageFont.truetype("app/image/assets/whitney-medium.ttf", 60)
    fntt = ImageFont.truetype("app/image/assets/whitney-medium.ttf", 30)
    if len(text) > 1000:
        print("text too long")
    else:
        user_color = (256,256,256) if dark else (6,6,7) 
        d.text((260, 70), username, fill=user_color, font=fntd)
        wi = fntd.getsize(username)
        ##72767d
        d.text((300 + wi[0], 87), t_string, fill=(114, 118, 125, 50), font=fntt)
        wrap = WriteText(y)
        #dark: #ffffff light:
        text_color = (256,256,256) if dark else (46,51,56) 
        f = wrap.write_text_box(
            260,
            80,
            text,
            2120,
            "app/image/assets/whitney-medium.ttf",
            50,
            color=text_color,
        )
        print(f)
        im = wrap.ret_img()
        #dark: #36393f or lighr; #ffffff
        ima = im.crop((0, 0, 2400, (f + 90)))
        return ima
