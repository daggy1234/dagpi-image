import time

from typing import Callable, Awaitable
from fastapi import Request, Response


async def add_process_time_header(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
