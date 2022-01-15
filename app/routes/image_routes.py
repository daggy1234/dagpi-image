from fastapi import APIRouter, Response

from app.image.numpy_manip import *
from app.image.pil_manipulation import *
from app.image.retro_meme import *
from app.image.text_images import *
from app.image.polaroid_manip import glitch
from app.image.PILManip import pil, static_pil, pil_multi_image
from app.image.WandManip import wand
from app.image.NumpyManip import numpy
from app.image.decorators import byt_to_byt
from app.image.wand_manipulation import *
from app.routes.responses import (gif_response_only, normal_response,
                                  static_response_only)
from app.utils.client import Client

router: APIRouter = APIRouter()


@router.get("/mirror/", responses=normal_response)
async def mirror_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await pil(mirror, byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/flip/", responses=normal_response)
async def flip_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await pil(flip, byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/colors/", responses=static_response_only)
async def color_image(url: str):
    byt = await Client.image_bytes(url)
    img = await static_pil(top5colors, byt)
    return Response(img.read(), media_type="image/png")


@router.get("/retromeme/", responses=static_response_only)
async def retro_meme(url: str, top_text: str, bottom_text: str):
    byt = await Client.image_bytes(url)
    text = top_text + "| " + bottom_text
    img, image_format = await pil(retromeme_gen, byt, text=text)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/motiv/", responses=static_response_only)
async def motiv_meme(url: str, top_text: str, bottom_text: str):
    byt = await Client.image_bytes(url)
    img = await static_pil(motiv, byt, top_text, bottom_text)
    return Response(img.read(), media_type="image/png")


@router.get("/modernmeme/", responses=normal_response)
async def modern_meme(url: str, text: str):
    byt = await Client.image_bytes(url)
    img, image_format = await pil(memegen, byt, text)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/triggered/", responses=gif_response_only)
async def trigger_image(url: str):
    byt = await Client.image_bytes(url)
    img = await byt_to_byt(triggered, byt)
    return Response(img.read(), media_type="image/gif")


@router.get("/expand/", responses=gif_response_only)
async def expand_image(url: str):
    byt = await Client.image_bytes(url)
    img = await byt_to_byt(expand, byt)
    return Response(img.read(), media_type="image/gif")


@router.get("/wasted/", responses=normal_response)
async def wasted_image(url: str):
    byt = await Client.image_bytes(url)
    img, _image_format = await wand(grayscale, byt)
    img, image_format = await pil(wasted, img.read())
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/5g1g/", responses=static_response_only)
async def get_5g1g(url: str, url2: str):
    byt = await Client.image_bytes(url)
    byt_b = await Client.image_bytes(url2)
    img = await pil_multi_image(five_guys_one_girl, byt, byt_b)
    return Response(img.read(), media_type="image/png")


@router.get("/whyareyougay/", responses=static_response_only)
async def get_why_are_you_gay(url: str, url2: str):
    byt = await Client.image_bytes(url)
    byt_b = await Client.image_bytes(url2)
    img = await pil_multi_image(why_are_you_gay, byt, byt_b)
    return Response(img.read(), media_type="image/png")


@router.get("/slap/", responses=static_response_only)
async def slap_image(url: str, url2: str):
    byt = await Client.image_bytes(url)
    byt_b = await Client.image_bytes(url2)
    img = await pil_multi_image(slap, byt, byt_b)
    return Response(img.read(), media_type="image/png")


@router.get("/invert/", responses=normal_response)
async def invert_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await pil(invert, byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/sobel/", responses=static_response_only)
async def sobel_image(url: str):
    byt = await Client.image_bytes(url)
    img = await numpy(get_sobel, byt)
    return Response(img.read(), media_type="image/png")


@router.get("/hog/", responses=static_response_only)
async def hog_image(url: str):
    byt = await Client.image_bytes(url)
    img = await byt_to_byt(hog_process, byt)
    return Response(img.read(), media_type="image/png")


@router.get("/triangle/", responses=static_response_only)
async def triange(url: str):
    byt = await Client.image_bytes(url)
    img = await byt_to_byt(triangle_manip, byt)
    return Response(img.read(), media_type="image/png")


@router.get("/blur/", responses=normal_response)
async def blur_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await pil(blur, byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/rgb/", responses=static_response_only)
async def rgb_image(url: str):
    byt = await Client.image_bytes(url)
    img = await byt_to_byt(rgb_graph, byt)
    return Response(img.read(), media_type="image/png")


@router.get("/angel/", responses=normal_response)
async def angel_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await pil(angel, byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/lego/", responses=normal_response)
async def lego_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await pil(lego, byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/satan/", responses=normal_response)
async def sat_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await pil(satan, byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/hitler/", responses=normal_response)
async def hit_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await pil(htiler, byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/obama/", responses=normal_response)
async def obama_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await pil(obama, byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/wanted/", responses=normal_response)
async def wanted_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await pil(wanted, byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/shatter/", responses=normal_response)
async def shatter_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await pil(shatter, byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/bad/", responses=normal_response)
async def bad_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await pil(bad_img, byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/sith/", responses=normal_response)
async def sith_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await pil(sithlord, byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/jail/", responses=normal_response)
async def jail_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await pil(jail, byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/gay/", responses=normal_response)
async def gay_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await pil(gay, byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/burn/", responses=normal_response)
async def burn(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await pil(molten, byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/earth/", responses=normal_response)
async def earth_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await pil(earth, byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/freeze/", responses=normal_response)
async def freeze(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await pil(ice, byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/ground/", responses=normal_response)
async def ground(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await pil(earth, byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/comic/", responses=normal_response)
async def comic(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await pil(comic_manip, byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/glitch/", responses=static_response_only)
async def glitch_image(url: str):
    byt = await Client.image_bytes(url)
    img = await glitch(byt)
    return Response(img.read(), media_type="image/png")


@router.get("/pride/", responses=normal_response)
async def pride_image(url: str, flag: str):
    byt = await Client.image_bytes(url)
    img, image_format = await pil(pride, byt, flag)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/trash/", responses=normal_response)
async def trash_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await pil(trash, byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/fedora/", responses=normal_response)
async def fedora_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await pil(fedora, byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/delete/", responses=normal_response)
async def delete_image(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await pil(delete, byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/pixel/", responses=normal_response)
async def pixel_route(url: str, scale: int = 32):
    byt = await Client.image_bytes(url)
    img, image_format = await pil(pixelate, byt, scale)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/deepfry/", responses=normal_response)
async def test_app(url: str):
    byt = await Client.image_bytes(url)
    img, image_format = await pil(deepfry, byt)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/mosiac/", responses=normal_response)
async def mosiac_manip(url: str, pixels: int = 16):
    byt = await Client.image_bytes(url)
    img, image_format = await pil(mosiac, byt, pixels)
    return Response(img.read(), media_type=f"image/{image_format}")


@router.get("/ascii/", responses=static_response_only)
async def asc_image(url: str):
    byt = await Client.image_bytes(url)
    img = await static_pil(ascii_image, byt)
    return Response(img.read(), media_type="image/png")


@router.get("/stringify/", responses=static_response_only)
async def stri_image(url: str):
    byt = await Client.image_bytes(url)
    img = await static_pil(stringify, byt)
    return Response(img.read(), media_type="image/png")


@router.get("/floor/", responses=normal_response)
async def floor_image(url: str):
    byt = await Client.image_bytes(url)
    img, img_format = await wand(floor, byt)
    return Response(img.read(), media_type=f"image/{img_format}")


@router.get("/charcoal/", responses=normal_response)
async def charcoal_image(url: str):
    byt = await Client.image_bytes(url)
    img, img_format = await wand(charcoal, byt)
    return Response(img.read(), media_type=f"image/{img_format}")


@router.get("/poster/", responses=normal_response)
async def poster_image(url: str):
    byt = await Client.image_bytes(url)
    img, img_format = await wand(poster, byt)
    return Response(img.read(), media_type=f"image/{img_format}")


@router.get("/sepia/", responses=normal_response)
async def sepia_image(url: str):
    byt = await Client.image_bytes(url)
    img, img_format = await wand(sepia, byt)
    return Response(img.read(), media_type=f"image/{img_format}")


@router.get("/polaroid/", responses=normal_response)
async def polar_image(url: str):
    byt = await Client.image_bytes(url)
    img, img_format = await wand(polaroid, byt)
    return Response(img.read(), media_type=f"image/{img_format}")


@router.get("/swirl/", responses=normal_response)
async def swirl_image(url: str):
    byt = await Client.image_bytes(url)
    img, img_format = await wand(swirl, byt)
    return Response(img.read(), media_type=f"image/{img_format}")


@router.get("/paint/", responses=normal_response)
async def paint_image(url: str):
    byt = await Client.image_bytes(url)
    img, img_format = await wand(paint, byt)
    return Response(img.read(), media_type=f"image/{img_format}")


@router.get("/night/", responses=normal_response)
async def night_image(url: str):
    byt = await Client.image_bytes(url)
    img, img_format = await wand(night, byt)
    return Response(img.read(), media_type=f"image/{img_format}")


# @router.get("/solar/", responses=normal_response)
# async def solar_image(url: str):
#     byt = await Client.image_bytes(url)
#     img, img_format = await solar, byt)
#     return Response(img.read(), media_type=f"image/{img_format}")


@router.get("/america/", responses=gif_response_only)
async def america_image(url: str):
    byt = await Client.image_bytes(url)
    img = await byt_to_byt(america, byt)
    return Response(img.read(), media_type="image/gif")


@router.get("/sketch/", responses=gif_response_only)
async def sketch_image(url: str):
    byt = await Client.image_bytes(url)
    img = await byt_to_byt(quantize, byt)
    return Response(img.read(), media_type="image/gif")


@router.get("/spin/", responses=gif_response_only)
async def spin_image(url: str):
    byt = await Client.image_bytes(url)
    img = await byt_to_byt(spin_manip, byt)
    return Response(img.read(), media_type="image/gif")


@router.get("/petpet/", responses=gif_response_only)
async def pet_pet_image(url: str):
    byt = await Client.image_bytes(url)
    img = await byt_to_byt(petpetgen, byt)
    return Response(img.read(), media_type="image/gif")


@router.get("/dissolve/", responses=gif_response_only)
async def dissolve(url: str, transparent: bool = False):
    byt = await Client.image_bytes(url)
    img = await byt_to_byt(gen_dissolve, byt, transparent=transparent)
    return Response(img.read(), media_type="image/gif")


@router.get("/communism/", responses=gif_response_only)
async def commie_image(url: str):
    byt = await Client.image_bytes(url)
    img = await byt_to_byt(communism, byt)
    return Response(img.read(), media_type="image/gif")


@router.get("/thoughtimage/", responses=normal_response)
async def get_thought_image(url: str, text: str):
    byt = await Client.image_bytes(url)
    img, img_format = await pil(thought_image, byt, text)
    return Response(img.read(), media_type=f"image/{img_format}")


@router.get("/captcha/", responses=normal_response)
async def get_captcha_image(url: str, text: str):
    byt = await Client.image_bytes(url)
    img = await static_pil(captcha, byt, text)
    return Response(img.read(), media_type="image/png")


@router.get("/tweet/", responses=static_response_only)
async def tweet(url: str, username: str, text: str):
    byt = await Client.image_bytes(url)
    img = await static_pil(tweet_gen, byt, username, text)
    return Response(img.read(), media_type="image/png")


@router.get("/rainbow/", responses=normal_response)
async def rainbow_manip(url: str):
    byt = await Client.image_bytes(url)
    img, img_format = await wand(rainbow, byt)
    return Response(img.read(), media_type=f"image/{img_format}")


@router.get("/magik/", responses=normal_response)
async def magic(url: str, scale: int = None):
    byt = await Client.image_bytes(url)
    img, img_format = await wand(magik, byt, scale)
    return Response(img.read(), media_type=f"image/{img_format}")


@router.get("/discord/", responses=static_response_only)
async def discord_quote(url: str, username: str, text: str, dark: bool = True):
    byt = await Client.image_bytes(url)
    img = await static_pil(quote, byt, username, text, dark)
    return Response(img.read(), media_type="image/png")


@router.get("/yt/", responses=static_response_only)
async def youtube_comment(url: str,
                          username: str,
                          text: str,
                          dark: bool = True):
    byt = await Client.image_bytes(url)
    img = await static_pil(yt_comment, byt, username, text, dark)
    return Response(img.read(), media_type="image/png")


@router.get("/neon/", responses=normal_response)
async def neon_image(url: str,
                     sharp: bool = True,
                     soft: bool = True,
                     overlay: bool = False,
                     multi: bool = False,
                     gradient: int = 0,
                     per_color: int = None,
                     colors_per_frame: int = None,
                     direction: str = 'right',
                     colors=None):
    if colors is None:
        colors = [(244, 40, 43), (241, 196, 15), (56, 244, 120),
                  (52, 152, 249), (180, 49, 182)]
    animated = multi or len(colors) > 1
    byt = await Client.image_bytes(url)
    img = await byt_to_byt(neon,
                           byt,
                           colors=colors,
                           multi=multi,
                           sharp=sharp,
                           soft=soft,
                           overlay=overlay,
                           direction=direction,
                           gradient=gradient,
                           per_color=per_color,
                           colors_per_frame=colors_per_frame)
    return Response(img.read(),
                    media_type=f"image/{'gif' if animated else 'png'}")


@router.get("/bomb/", responses=gif_response_only)
async def bomb_gif(url: str):
    byt = await Client.image_bytes(url)
    img = await byt_to_byt(bomb, byt)
    return Response(img.read(), media_type="image/gif")


# @router.get("/flash/", responses=gif_response_only)
# async def flash_gif(url: str):
#     byt = await Client.image_bytes(url)
#     img = await flash, byt)
#     return Response(img.read(), media_type="image/gif")


@router.get("/shake/", responses=gif_response_only)
async def shake_gif(url: str):
    byt = await Client.image_bytes(url)
    img = await byt_to_byt(shake, byt)
    return Response(img.read(), media_type="image/gif")


@router.get("/bonk/", responses=gif_response_only)
async def bonk_gif(url: str):
    byt = await Client.image_bytes(url)
    img = await byt_to_byt(bonk, byt)
    return Response(img.read(), media_type="image/gif")


@router.get("/cube/", responses=normal_response)
async def cube_image(url: str):
    byt = await Client.image_bytes(url)
    img, img_format = await wand(cube, byt)
    return Response(img.read(), media_type=f"image/{img_format}")
