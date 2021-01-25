from fastapi import Request
from fastapi.responses import JSONResponse

from app.utils.client import Client


async def auth_check(request: Request, call_next):
    if (request.url.path == "/") or (request.url.path == "/metrics/") or \
            (request.url.path == "/docs") or \
            (request.url.path == "/openapi.json") or \
            (request.url.path == "/image/openapi.json") or \
            (request.url.path == "/playground"):
        response = await call_next(request)
        return response
    else:
        try:
            token = request.headers["Authorization"]
        except KeyError:
            return JSONResponse({"message": "Unauthorized"}, status_code=403)

        tok = await Client.auth(token)
        if tok.auth:
            if not tok.ratelimited:
                response = await call_next(request)
                return response
            return JSONResponse({"message": "Ratelimited"}, status_code=429)

        return JSONResponse({"message": "Unauthorized"}, status_code=403)
