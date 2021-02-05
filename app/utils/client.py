import asyncio
import os
import re
import urllib.parse
from typing import Dict

import httpx
from async_timeout import timeout

from ..exceptions.errors import BadUrl, NoImageFound, ServerTimeout

headers = {'Authorization': os.getenv("TOKEN", "What")}
base_url = os.getenv("BASE_URL", "https://dagbot.daggy.tech")
print(headers, base_url)
_session = None


async def get_session():
    global _session
    if _session is None:
        _session = httpx.AsyncClient(headers=headers)
    return _session


class AuthModel:

    def __init__(self, obj: Dict):
        self.auth = obj.get("auth")
        self.ratelimited = obj.get("ratelimited")
        self.premium = obj.get("premium")
        self.ratelimit = int(obj.get("ratelimit"))
        self.left = int(obj.get("left"))


class Client:

    @staticmethod
    async def auth(token: str):
        session = await get_session()
        print(f"{base_url}/auth/{token}")
        r = await session.get(f"{base_url}/auth/{token}")
        return AuthModel(r.json())

    @staticmethod
    async def post_stat(route: str, token: str, ua: str):
        session = await get_session()
        js = {
            "api": "image",
            "route": route,
            "token": token,
            "user_agent": ua

        }
        r = await session.post(f"{base_url}/statpost", json=js)
        print(r.status_code)

    @staticmethod
    async def image_bytes(url: str):
        url = urllib.parse.unquote(url)
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)'
            r'+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        r = (re.match(regex, url) is not None)
        if not r:
            raise BadUrl('Your url is malformed')
        session = await get_session()
        try:
            async with timeout(10):
                try:
                    r = await session.get(url)
                    if r.status_code == 200:
                        byt: bytes = r.read()
                        return byt
                    else:
                        raise NoImageFound("Non 200 Status Code")
                except httpx.RequestError:
                    raise NoImageFound("Requesting Error")
        except asyncio.TimeoutError:
            raise ServerTimeout("Server Timed Out")
