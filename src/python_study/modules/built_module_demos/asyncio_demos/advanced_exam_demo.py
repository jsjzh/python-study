import asyncio
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum
import random
from typing import Any

from python_study.utils import fake_fetch


class CrawlStatus(Enum):
    SUCCESS = "success"
    TIMEOUT = "timeout"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class CrawlTask:
    task_id: int
    url: str


@dataclass(frozen=True)
class CrawlResult:
    task_id: int
    url: str
    status: CrawlStatus
    body: str | None
    error: str | None
    retries: int


async def simple_fake_fetch(
    url: str,
    sem: asyncio.Semaphore,
    event: asyncio.Event,
    min_delay: float = 0.2,
    max_delay: float = 0.8,
    timeout: float = 1,
    fail: bool = False,
) -> str | None:
    async with sem:
        print(f"----- start fetch {url} -----")
        async with asyncio.timeout(timeout):
            await asyncio.sleep(random.uniform(min_delay, max_delay))
            if fail:
                raise RuntimeError(f"timeout {url}")
            else:
                event.set()
                return f"data-{url}"


class AsyncRateLimitedCrawler(object):
    def __init__(
        self, sem_count: int, rate_count: int, timeout: float, retry_count: int
    ) -> None:
        self._sem = asyncio.Semaphore(sem_count)
        self._queue = asyncio.Queue[CrawlTask](rate_count)
        self._timeout = timeout
        self._retry_count = retry_count
        self._tasks: dict[int, Any] = {}

        # asyncio.create_task(self.start())
        asyncio.create_task(self.watch())

    async def watch(self) -> None:
        while True:
            pass

    # async def start(self) -> None:
    #     while True:
    #         ctask = await self._queue.get()
    #         event = asyncio.Event()
    #         print(f"start: {ctask.url}")
    #         task = asyncio.create_task(
    #             simple_fake_fetch(url=ctask.url, sem=self._sem, event=event)
    #         )

    #         await event.wait()

    #         print(f"----- task.result(): {task.result()} -----")

    async def crawl(self, tasks: Iterable[CrawlTask]) -> list[CrawlResult]:
        for task in tasks:
            event = asyncio.Event()
            self._tasks[task.task_id] = asyncio.create_task(
                simple_fake_fetch(url=task.url, sem=self._sem, event=event)
            )

        return []

    async def cancel(self) -> None:
        pass


async def run() -> None:
    # sem = asyncio.Semaphore(3)

    # async with asyncio.TaskGroup() as tg:
    #     tasks = [
    #         tg.create_task(simple_fake_fetch(f"url-{id}", sem=sem))
    #         for id in range(1, 10)
    #     ]

    # for task in tasks:
    #     print(f"----- result: {task.result()} -----")

    crawler = AsyncRateLimitedCrawler(
        sem_count=3, rate_count=3, timeout=5.0, retry_count=5
    )

    await crawler.crawl([CrawlTask(task_id=id, url=f"url-{id}") for id in range(1, 6)])
    await asyncio.sleep(3)
    await crawler.crawl([CrawlTask(task_id=id, url=f"url-{id}") for id in range(6, 11)])


def main() -> None:
    asyncio.run(run())
