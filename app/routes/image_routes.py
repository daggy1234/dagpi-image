from fastapi import APIRouter, Response

from app.image.retro_meme import *
from app.image.numpy_manip import *
from app.image.text_images import *
from app.image.pil_manipulation import *
from app.image.wand_manipulation import *
from app.utils.client import Client

router = APIRouter()


@router.get("/colors/")
async def color_image(url: str):
    byt = await Client.image_bytes(url)
    img = await top5colors(byt)
    return Response(img.read(), media_type="image/png")


@router.get("/retromeme/")
async def retro_meme(url: str, text: str):
    byt = await Client.image_bytes(url)
    img, image_format = await retromeme_gen(byt, text)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/triggered/")
async def trigger_image(url: str):
    byt = await Client.image_bytes(url)
    img = await triggered(byt)
    return Response(img.read(), media_type="image/gif")


@router.get("/wasted/")
async def wasted_image(url: str):
    byt = await Client.image_bytes(url)
    img, _image_format = await grayscale(byt)
    img, image_format = await wasted(img.read())
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/5g1g/")
async def get_5g1g(url: str, url2: str):
    byt = await Client.image_bytes(url)
    byt_b = await Client.image_bytes(url2)
    img = await five_guys_one_girl(byt, byt_b)
    return Response(img.read(), media_type="image/png")


@router.get("/whyareyougay/")
async def get_why_are_you_gay(url: str, url2: str):
    byt = await Client.image_bytes(url)
    byt_b = await Client.image_bytes(url2)
    img = await why_are_you_gay(byt, byt_b)
    return Response(img.read(), media_type="image/png")


@router.get("/invert/")
async def invert_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await invert(byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/sobel/")
async def sobel_image(url: str):
    byt = await Client.image_bytes(url)
    img = await get_sobel(byt)
    return Response(img.read(), media_type="image/png")


@router.get("/hog/")
async def hog_image(url: str):
    byt = await Client.image_bytes(url)
    img = await hog_process(byt)
    return Response(img.read(), media_type="image/png")


@router.get("/blur/")
async def blur_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await blur(byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/rgb/")
async def rgb_image(url: str):
    byt = await Client.image_bytes(url)
    img = await rgb_graph(byt)
    return Response(img.read(), media_type="image/png")


@router.get("/angel/")
async def angel_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await angel(byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/satan/")
async def sat_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await satan(byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/hitler/")
async def hit_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await htiler(byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/obama/")
async def obama_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await obama(byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/wanted/")
async def wanted_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await wanted(byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/bad/")
async def bad_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await bad_img(byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/sith/")
async def sith_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await sithlord(byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/jail/")
async def jail_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await jail(byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/gay/")
async def gay_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await gay(byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/trash/")
async def trash_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await trash(byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/pixel/")
async def pixel_route(url: str = "https://dagbot-is.the-be.st/logo.png"):
    byt = await Client.image_bytes(url)
    img, image_format = await pixelate(byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/deepfry/")
async def test_app(url: str = "https://dagbot-is.the-be.st/logo.png"):
    byt = await Client.image_bytes(url)
    img, image_format = await deepfry(byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/ascii/")
async def asc_image(url: str):
    byt = await Client.image_bytes(url)
    img = await ascii_image(byt)
    return Response(img.read(), media_type="image/png")


@router.get("/floor/")
async def floor_image(url: str):
    byt = await Client.image_bytes(url)
    img, img_format = await floor(byt)
    return Response(img.read(), media_type=f"image/{img_format}")


@router.get("/charcoal/")
async def charcoal_image(url: str):
    byt = await Client.image_bytes(url)
    img, img_format = await charcoal(byt)
    return Response(img.read(), media_type=f"image/{img_format}")


@router.get("/poster/")
async def poster_image(url: str):
    byt = await Client.image_bytes(url)
    img, img_format = await poster(byt)
    return Response(img.read(), media_type=f"image/{img_format}")


@router.get("/sepia/")
async def sepia_image(url: str):
    byt = await Client.image_bytes(url)
    img, img_format = await sepia(byt)
    return Response(img.read(), media_type=f"image/{img_format}")


@router.get("/polaroid/")
async def polar_image(url: str):
    byt = await Client.image_bytes(url)
    img, img_format = await polaroid(byt)
    return Response(img.read(), media_type=f"image/{img_format}")


@router.get("/swirl/")
async def swirl_image(url: str):
    byt = await Client.image_bytes(url)
    img, img_format = await swirl(byt)
    return Response(img.read(), media_type=f"image/{img_format}")


@router.get("/paint/")
async def paint_image(url: str):
    byt = await Client.image_bytes(url)
    img, img_format = await paint(byt)
    return Response(img.read(), media_type=f"image/{img_format}")


@router.get("/night/")
async def night_image(url: str):
    byt = await Client.image_bytes(url)
    img, img_format = await night(byt)
    return Response(img.read(), media_type=f"image/{img_format}")


@router.get("/solar/")
async def solar_image(url: str):
    byt = await Client.image_bytes(url)
    img, img_format = await solar(byt)
    return Response(img.read(), media_type=f"image/{img_format}")


@router.get("/thoughtimage/")
async def get_thought_image(url: str, text: str):
    byt = await Client.image_bytes(url)
    img, img_format = await thought_image(byt, text)
    return Response(img.read(), media_type=f"image/{img_format}")


@router.get("/tweet/")
async def tweet(url: str, username: str, text: str):
    byt = await Client.image_bytes(url)
    img = await tweet_gen(byt, username, text)
    return Response(img.read(), media_type="image/png")


@router.get("/discord/")
async def discord_quote(url: str, username: str, text: str):
    byt = await Client.image_bytes(url)
    img = await quote(byt, username, text)
    return Response(img.read(), media_type="image/png")
