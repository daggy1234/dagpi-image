from __future__ import annotations
import functools
from typing import Callable, TypeVar, Awaitable, TYPE_CHECKING
from concurrent import futures
import asyncio
from app.exceptions.errors import ManipulationError

if TYPE_CHECKING:
    from typing_extensions import ParamSpec
    P = ParamSpec('P')
else:
    P = TypeVar('P')

R = TypeVar("R")


def executor(function: Callable[P, R]) -> Callable[P, Awaitable[R]]:
    @functools.wraps(function)
    def decorator(*args: P.args, **kwargs: P.kwargs) -> Awaitable[R]:
        try:
            partial = functools.partial(function, *args, **kwargs)
            loop = asyncio.get_event_loop()
            return loop.run_in_executor(futures.ThreadPoolExecutor(), partial)
        except Exception as e:
            raise ManipulationError(str(e))

    return decorator
