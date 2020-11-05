import asyncio
import os
import re
from typing import Dict

import httpx
from async_timeout import timeout

from ..exceptions.errors import BadUrl, NoImageFound, ServerTimeout

headers = {'Authorization': os.getenv("TOKEN")}
base_url = os.getenv("BASE_URL")
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


class Client:

    @staticmethod
    async def auth(token: str):
        session = await get_session()
        r = await session.get(f"{base_url}/auth/{token}")
        return AuthModel(r.json())

    @staticmethod
    async def image_bytes(url: str):
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
                        raise NoImageFound()
                except httpx.RequestError:
                    raise NoImageFound()
        except asyncio.TimeoutError:
            raise ServerTimeout()
