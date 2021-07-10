from fastapi.responses import JSONResponse
from starlette.background import BackgroundTasks
from typing import Callable, Awaitable
from fastapi import Request, Response
from app.utils.client import Client


async def post_stat(route: str, token: str, ua: str) -> None:
    await Client.post_stat(route, token, ua)


async def auth_check(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    if request.url.path in [
            "/", "/metrics/", "/docs", "/openapi.json", "/image/openapi.json",
            "/playground"
    ]:
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
                response.headers["X-RateLimit-Limit"] = str(tok.ratelimit)
                response.headers['X-RateLimit-Remaining'] = str(tok.left)
                response.headers['X-RateLimit-Reset'] = str(tok.reset)
                t = BackgroundTasks()
                try:
                    ua = request.headers.get("user-agent")
                except KeyError:
                    ua = "No User Agent"
                t.add_task(post_stat,
                           route=request.url.path,
                           token=token,
                           ua=ua)
                response.background = t
                return response
            return JSONResponse({"message": "Ratelimited"},
                                headers={
                                    'X-RateLimit-Limit': str(tok.ratelimit),
                                    'X-RateLimit-Remaining': str(tok.left),
                                    'X-RateLimit-Reset': str(tok.reset)
                                },
                                status_code=429)

        return JSONResponse({"message": "Unauthorized"}, status_code=403)
