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
    RETRY_LIMIT = "retry_limit"


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
        # TODO
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

        self._tasks: list[asyncio.Task[CrawlResult]] = []
        self._task_results: dict[int, CrawlResult] = {}

    async def _fetch(
        self,
        task: CrawlTask,
        fail: bool = False,
    ) -> CrawlResult:
        async with self._sem:
            pre_task = self._task_results.get(task.task_id)

            if pre_task:
                if self._retry_count == pre_task.retries:
                    return CrawlResult(
                        task_id=task.task_id,
                        url=task.url,
                        status=CrawlStatus.RETRY_LIMIT,
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

    async def crawl(self, crawl_tasks: Iterable[CrawlTask]) -> list[CrawlResult]:
        results: list[CrawlResult] = []
        retry_tasks: list[CrawlResult] = []
        retry_results: list[CrawlResult] = []

        async with asyncio.TaskGroup() as tg:
            tasks = [
                tg.create_task(
                    self._fetch(task=task, fail=random.choice([False, True]))
                )
                for task in crawl_tasks
            ]

            self._tasks += tasks

        for task in tasks:
            result = task.result()

            self._task_results[result.task_id] = result

            match result.status:
                case CrawlStatus.FAILED:
                    retry_tasks.append(result)
                case _:
                    results.append(result)

        if len(retry_tasks):
            retry_results = await self.crawl(
                [CrawlTask(task_id=task.task_id, url=task.url) for task in retry_tasks]
            )

        return [*results, *retry_results]

    async def cancel(self) -> None:
        pass


async def run() -> None:
    crawler = AsyncRateLimitedCrawler(
        sem_count=3,
        rate_count=3,
        retry_count=1,
        timeout=0.6,
        min_delay=0.2,
        max_delay=0.8,
    )

    datas = await crawler.crawl(
        [CrawlTask(task_id=id, url=f"url-{id}") for id in range(1, 11)]
    )

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
