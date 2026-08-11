import asyncio
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum
import random


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


class AsyncRateLimitedCrawler(object):
    def __init__(
        self,
        sem_count: int,
        rate_count: int,
        retry_count: int,
        timeout: float,
        min_delay: float = 0.2,
        max_delay: float = 0.8,
    ) -> None:
        self._sem = asyncio.Semaphore(sem_count)

        self._timeout = timeout
        self._retry_count = retry_count
        self._min_delay = min_delay
        self._max_delay = max_delay

        self._cancelled = False

        self._rate_count = rate_count
        self._token_queue: asyncio.Queue[None] = asyncio.Queue(maxsize=1)
        self._token_queue_task: asyncio.Task[None] | None = None

        self._tasks: list[asyncio.Task[CrawlResult]] = []
        self._task_results: dict[int, CrawlResult] = {}

    async def _start_token_queue(self) -> None:
        while True:
            await self._token_queue.put(None)
            await asyncio.sleep(1.0 / self._rate_count)

    async def _fetch(
        self,
        task: CrawlTask,
        fail: bool = False,
    ) -> CrawlResult:
        if self._cancelled:
            return CrawlResult(
                task_id=task.task_id,
                url=task.url,
                status=CrawlStatus.CANCELLED,
                body=None,
                error=f"fetch error cancel",
                retries=0,
            )

        pre_task = self._task_results.get(task.task_id)

        try:
            await self._token_queue.get()

            async with self._sem:
                if pre_task:
                    if self._retry_count == pre_task.retries:
                        return CrawlResult(
                            task_id=task.task_id,
                            url=task.url,
                            status=CrawlStatus.FAILED,
                            body=None,
                            error=f"fetch error retry limit",
                            retries=pre_task.retries,
                        )

                    wait_time = 0.5 * pow(2, pre_task.retries)

                    print(
                        f"[task id: {task.task_id}] retry {pre_task.retries + 1} wait {wait_time}s fetching..."
                    )
                    await asyncio.sleep(wait_time)
                else:
                    print(f"[task id: {task.task_id}] fetching...")

                try:
                    async with asyncio.timeout(self._timeout):
                        await asyncio.sleep(
                            random.uniform(self._min_delay, self._max_delay)
                        )
                        if fail:
                            return CrawlResult(
                                task_id=task.task_id,
                                url=task.url,
                                status=CrawlStatus.FAILED,
                                body=None,
                                error=f"fetch error fail",
                                retries=pre_task.retries + 1 if pre_task else 0,
                            )
                        else:
                            return CrawlResult(
                                task_id=task.task_id,
                                url=task.url,
                                status=CrawlStatus.SUCCESS,
                                body=f"fetch data {task.url}",
                                error=None,
                                retries=pre_task.retries + 1 if pre_task else 0,
                            )
                except TimeoutError:
                    return CrawlResult(
                        task_id=task.task_id,
                        url=task.url,
                        status=CrawlStatus.TIMEOUT,
                        body=None,
                        error=f"fetch error timeout",
                        retries=pre_task.retries + 1 if pre_task else 0,
                    )
        except asyncio.CancelledError:
            return CrawlResult(
                task_id=task.task_id,
                url=task.url,
                status=CrawlStatus.CANCELLED,
                body=None,
                error=f"fetch error cancel",
                retries=pre_task.retries + 1 if pre_task else 0,
            )

    async def crawl(self, crawl_tasks: Iterable[CrawlTask]) -> list[CrawlResult]:
        self._cancelled = False
        self._token_queue_task = asyncio.create_task(self._start_token_queue())

        pending: list[CrawlTask] = list(crawl_tasks)
        results: list[CrawlResult] = []
        attempts = 0

        try:
            while pending and attempts <= self._retry_count:

                if self._cancelled:
                    break

                batch: list[asyncio.Task[CrawlResult]] = [
                    asyncio.create_task(
                        self._fetch(t, fail=random.choice([False, True]))
                    )
                    for t in pending
                ]

                self._tasks.extend(batch)

                batch_results = await asyncio.gather(*batch)

                retry_pending: list[CrawlTask] = []

                for r in batch_results:
                    if r.status == CrawlStatus.FAILED:
                        self._task_results[r.task_id] = r
                        retry_pending.append(CrawlTask(task_id=r.task_id, url=r.url))
                    else:
                        results.append(r)

                pending = retry_pending
                attempts += 1
        finally:
            self._token_queue_task.cancel()

        return results

    async def cancel(self) -> None:
        self._cancelled = True

        if self._token_queue_task is not None:
            self._token_queue_task.cancel()

        for task in self._tasks:
            if not task.done():
                task.cancel()


async def run() -> None:
    crawler = AsyncRateLimitedCrawler(
        sem_count=3,
        rate_count=3,
        retry_count=1,
        timeout=0.6,
        min_delay=0.2,
        max_delay=0.8,
    )

    crawl_task = asyncio.create_task(
        crawler.crawl([CrawlTask(task_id=id, url=f"url-{id}") for id in range(1, 11)])
    )

    await asyncio.sleep(10)
    await crawler.cancel()

    datas = await crawl_task

    print()

    for data in datas:
        match data.status:
            case CrawlStatus.SUCCESS:
                print(
                    f"[task id: {data.task_id}] status: {data.status.value} retry: {data.retries} body: {data.body}"
                )
            case _:
                print(
                    f"[task id: {data.task_id}] status: {data.status.value} retry: {data.retries} error: {data.error}"
                )


def main() -> None:
    asyncio.run(run())
