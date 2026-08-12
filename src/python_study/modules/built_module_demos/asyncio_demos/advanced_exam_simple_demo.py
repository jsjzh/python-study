import asyncio
from collections.abc import Awaitable, Callable
import json
import random
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def retry_async(
    max_retries: int = 3, base_delay: float = 0.5, timeout: float | None = None
) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
    if max_retries < 0:
        raise ValueError(f"max_retries 必须大于等于 0")

    def wrap_wrapper(afunc: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:

            for current_count in range(max_retries + 1):
                try:
                    async with asyncio.timeout(timeout):
                        return await afunc(*args, **kwargs)
                except asyncio.CancelledError:
                    raise
                except Exception as error:
                    if current_count == max_retries:
                        raise
                    delay = random.uniform(0, base_delay * 2**current_count)
                    print(
                        f"----- {afunc.__name__} 第 {current_count + 1}/{max_retries + 1} 次失败 "
                        f"({type(error).__name__}: {error})，等待 {delay:.2f}s 后重试 -----"
                    )
                    await asyncio.sleep(delay)

            raise RuntimeError(
                "unreachable: retry loop exited without returning or raising"
            )

        return wrapper

    return wrap_wrapper


@retry_async(max_retries=3, base_delay=0.5, timeout=0.5)
async def fetch(url: str) -> str:
    print(f"fetching: {url}")
    await asyncio.sleep(random.uniform(0.2, 1.0))
    return json.dumps({"url": url})


async def run() -> None:
    try:
        data = await fetch(url="http://www.example.com")
        print(f"data: {data}")
    except Exception as error:
        print(f"error: {error}")


def main() -> None:
    asyncio.run(run())
