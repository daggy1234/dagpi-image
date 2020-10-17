import asyncio
import functools

from app.exceptions.errors import ManipulationError


def executor(function):
    @functools.wraps(function)
    def decorator(*args, **kwargs):
        try:
            partial = functools.partial(function, *args, **kwargs)
            loop = asyncio.get_event_loop()
            future = loop.run_in_executor(None, partial)
            return future
        except Exception as e:
            raise ManipulationError()

    return decorator
