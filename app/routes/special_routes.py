from fastapi import APIRouter, Response
from app.utils.client import Client
from app.image.special_manip import *
from app.routes.responses import gif_response_only


router = APIRouter()

@router.get("/special/", responses=gif_response_only)
async def retro_meme(url: str):
    byt = await Client.image_bytes(url)
    img = await special(byt)
    return Response(img.read(), media_type=f"image/gif")