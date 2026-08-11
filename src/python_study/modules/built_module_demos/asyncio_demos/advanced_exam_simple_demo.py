import asyncio
from collections.abc import Awaitable, Callable, Coroutine
from typing import Any, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def retry_async(
    max_retries: int = 3, base_delay: float = 0.5, timeout: float | None = None
) -> Callable[..., Any]:

    def wrap_wrapper(func: Any) -> Callable[P, Any]:

        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> None:
            try:
                async with asyncio.timeout(timeout):
                    return await func(*args, **kwargs)
            except TimeoutError:
                raise

        return wrapper

    return wrap_wrapper


@retry_async(max_retries=3, base_delay=0.5, timeout=0.1)
async def fetch(url: str) -> str:
    await asyncio.sleep(1)
    return f"data-{url}"


async def run() -> None:
    data = await fetch("url")
    print(f"----- data: {data} -----")


def main() -> None:
    asyncio.run(run())
