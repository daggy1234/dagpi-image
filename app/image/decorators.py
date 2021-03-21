import asyncio
import functools
from concurrent import futures

from app.exceptions.errors import ManipulationError


def executor(function):
    @functools.wraps(function)
    def decorator(*args, **kwargs):
        try:
            partial = functools.partial(function, *args, **kwargs)
            loop = asyncio.get_event_loop()
            return loop.run_in_executor(futures.ThreadPoolExecutor(), partial)
        except Exception as e:
            raise ManipulationError(str(e))

    return decorator
