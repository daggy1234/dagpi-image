import asyncio
import os
import re
import urllib.parse
from typing import Dict, TypedDict
import httpx
from async_timeout import timeout

from ..exceptions.errors import BadUrl, NoImageFound, ServerTimeout

headers: Dict[str, str] = {'Authorization': os.getenv("TOKEN", "token")}
base_url: str = os.getenv("BASE_URL", "https://dagpi.xyz")
print(headers, base_url)
_session = None


async def get_session() -> httpx.AsyncClient:
    global _session
    if _session is None:
        _session = httpx.AsyncClient()
    return _session


class AuthModelDict(TypedDict):
    auth: bool
    ratelimited: bool
    premium: bool
    ratelimit: int
    left: int
    after: int


class AuthModel:
    def __init__(self, obj: AuthModelDict):
        self.auth = obj["auth"]
        self.ratelimited = obj["ratelimited"]
        self.premium = obj["premium"]
        self.ratelimit = obj["ratelimit"]
        self.left = obj["left"]
        self.reset = obj["after"]


class Client:
    @staticmethod
    async def auth(token: str) -> AuthModel:
        session = await get_session()
        r = await session.get(f"{base_url}/auth/{token}", headers=headers)
        model: AuthModelDict = r.json()
        return AuthModel(model)

    @staticmethod
    async def post_stat(route: str, token: str, ua: str) -> None:
        session = await get_session()
        js = {"api": "image", "route": route, "token": token, "user_agent": ua}
        await session.post(f"{base_url}/statpost", json=js, headers=headers)

    @staticmethod
    async def image_bytes(url: str) -> bytes:
        url = urllib.parse.unquote(url)
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)'
            r'+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$',
            re.IGNORECASE)
        r = (re.match(regex, url) is not None)
        if not r:
            raise BadUrl('Your url is malformed')
        session = await get_session()
        try:
            async with timeout(10):
                try:
                    r = await session.get(url)
                    if r.status_code == 200:
                        return r.read()
                    else:
                        raise NoImageFound("Non 200 Status Code")
                except httpx.RequestError:
                    raise NoImageFound("Requesting Error")
        except asyncio.TimeoutError:
            raise ServerTimeout("Server Timed Out")
