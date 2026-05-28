import functools
import inspect
import time
from typing import Any, Callable

from loguru import logger


def timer(func: Callable[..., Any]) -> Callable[..., Any]:
    if inspect.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            start_time = time.perf_counter()
            result = await func(*args, **kwargs)
            logger.info(
                f"Function {func.__name__} completed in {time.perf_counter() - start_time:.5f} seconds"
            )
            return result

        return async_wrapper

    else:

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            logger.info(
                f"Function {func.__name__} completed in {time.perf_counter() - start_time:.5f} seconds"
            )
            return result

        return sync_wrapper
