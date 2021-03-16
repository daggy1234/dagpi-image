from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.background import BackgroundTasks

from app.utils.client import Client


async def post_stat(route: str, token: str, ua: str):
    await Client.post_stat(route, token, ua)


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
                response.headers["X-Ratelimit-Limit"] = str(tok.ratelimit)
                response.headers['X-Ratelimit-Remaining'] = str(tok.left)
                t = BackgroundTasks()
                try:
                    ua = request.headers.get("user-agent")
                except KeyError:
                    ua = "No User Agent"
                t.add_task(post_stat, route=request.url.path, token=token, ua=ua)
                response.background = t
                return response
            return JSONResponse({"message": "Ratelimited"}, headers={'X-Ratelimit-Limit': str(tok.ratelimit),
                                                                     'X-Ratelimit-Remaining': str(tok.left)},
                                status_code=429)

        return JSONResponse({"message": "Unauthorized"}, status_code=403)
