from fastapi import Request

from app.exceptions.errors import Unauthorised, RateLimit
from app.utils.client import Client


async def auth_check(request: Request, call_next):
    if (request.url.path == "/") or (request.url.path == "/metrics/") or \
            (request.url.path == "/docs") or (
            (request.url.path == "/openapi.json")):
        response = await call_next(request)
        return response
    else:
        try:
            token = request.headers["Authorization"]
        except KeyError:
            raise Unauthorised("No Token provided")

        tok = await Client.auth(token)
        if tok.auth:
            if not tok.ratelimited:
                response = await call_next(request)
                return response
            raise RateLimit("Too Many Requests")

        raise Unauthorised("Invalid Token")
