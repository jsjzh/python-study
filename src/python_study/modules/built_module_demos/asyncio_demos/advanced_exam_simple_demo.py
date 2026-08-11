import asyncio
from collections.abc import Awaitable, Callable, Coroutine
from typing import Any, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


# def retry_async(
#     max_retries: int = 3, base_delay: float = 0.5, timeout: float | None = None
# ) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
#     async def wrapper(*arg: R, **kwarg: R) -> None:
#         pass


async def run() -> None:
    pass


def main() -> None:
    asyncio.run(run())
