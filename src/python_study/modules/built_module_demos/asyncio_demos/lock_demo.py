import asyncio
from collections.abc import Callable, Coroutine
import random
from typing import Any, cast

from python_study.utils import fake_fetch


class AsyncCache(object):
    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._cache: dict[str, str] = {}
        self._pending: dict[str, asyncio.Future[str]] = {}

    def get(self, key: str) -> str | None:
        return self._cache.get(key, None)

    async def get_or_fetch(
        self,
        key: str,
        fetcher: Callable[[], Coroutine[Any, Any, str | None]],
    ) -> str | None:

        async with self._lock:
            if key in self._cache:
                return self._cache[key]

            if key in self._pending:
                future = self._pending[key]
                should_fetch = False
            else:
                future = asyncio.get_running_loop().create_future()
                self._pending[key] = future
                should_fetch = True

        if not should_fetch:
            return await future

        try:
            data = await fetcher()

            if data is None:
                raise ValueError(f"fetcher returned None for key={key}")

            async with self._lock:
                self._cache[key] = data
                del self._pending[key]

            future.set_result(data)

            return data

        except Exception as exc:
            async with self._lock:
                self._pending.pop(key, None)

            future.set_exception(exc)
            raise


async def run2() -> None:
    ac = AsyncCache()
    sem = asyncio.Semaphore(3)

    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(
                ac.get_or_fetch(
                    f"fetch-{random.randint(1, 20)}",
                    lambda: fake_fetch(index=random.randint(1, 20), sem=sem),
                )
            )
            for _ in range(1, 20)
        ]

    for i, t in enumerate(tasks):
        print(f"----- task[{i}] -> {t.result()} -----")


async def unsafe_increment(counter: dict[str, int], name: str) -> None:
    old = counter["value"]
    await asyncio.sleep(0)
    counter["value"] = old + 1
    print(f'----- {name}: {old} -> {counter["value"]} -----')


async def safe_increment(
    counter: dict[str, int], lock: asyncio.Lock, name: str
) -> None:
    async with lock:
        old = counter["value"]
        await asyncio.sleep(0)
        counter["value"] = old + 1
        print(f'----- {name}: {old} -> {counter["value"]} -----')


async def run() -> None:
    counter: dict[str, int] = {"value": 0}
    lock = asyncio.Lock()

    async with asyncio.TaskGroup() as tg:
        for i in range(5):
            tg.create_task(unsafe_increment(counter, f"unsafe{i}"))

    print(f'----- unsafe value {counter["value"]} -----')

    counter["value"] = 0
    async with asyncio.TaskGroup() as tg:
        for i in range(5):
            tg.create_task(safe_increment(counter, lock, f"unsafe{i}"))

    print(f'----- safe value {counter["value"]} -----')


def main() -> None:
    asyncio.run(run2())
