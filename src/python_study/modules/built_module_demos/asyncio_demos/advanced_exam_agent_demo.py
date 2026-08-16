"""
python_study.modules.built_module_demos.asyncio_demos.advanced_exam_agent_demo 的 Docstring

asyncio 期末考题：AsyncRateLimitedCrawler

实现一个异步限流爬虫，同时满足：
- 并发控制：Semaphore，同时最多 N 个请求在飞
- 速率限制：令牌桶（Token Bucket），每秒最多发出 R 个请求
- 超时保护：单请求超 T 秒自动取消，返回 TIMEOUT 标记而非抛异常
- 重试机制：非超时类失败自动重试最多 K 次，指数退避 0.5s / 1s / 2s ...
- 结果收集：crawl() 返回结构化结果列表
- 优雅关闭：cancel() 取消所有未完成任务，已完成的保留
- 类型安全：全部 dataclass / Enum 标注，禁止裸 Any
"""

import asyncio
import random
import time
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum
from typing import Protocol


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


class Fetcher(Protocol):
    async def __call__(self, url: str) -> str:
        """按 url 发起一次真实请求，成功返回响应体，失败抛异常。"""
        ...


class TokenBucket:
    """令牌桶限流器：以 rate 个/秒 的速率持续补充令牌，容量上限 capacity。"""

    def __init__(self, rate: float, capacity: int) -> None:
        if rate <= 0 or capacity < 1:
            raise ValueError("rate 必须 > 0，capacity 必须 >= 1")
        self._rate = rate
        self._capacity = capacity
        self._tokens = float(capacity)
        self._updated_at = time.monotonic()
        self._wakeup = asyncio.Event()
        self._wakeup.set()

    def _refill(self) -> None:
        now = time.monotonic()
        self._tokens = min(
            self._capacity, self._tokens + (now - self._updated_at) * self._rate
        )
        self._updated_at = now

    async def acquire(self) -> None:
        """取一个令牌；桶空则等待到足够令牌生成。可被 cancel() 打断。"""
        while True:
            self._refill()
            if self._tokens >= 1.0:
                self._tokens -= 1.0
                if self._tokens < 1.0:
                    self._wakeup.clear()
                return
            self._wakeup.clear()
            wait = (1.0 - self._tokens) / self._rate
            try:
                await asyncio.wait_for(self._wakeup.wait(), timeout=wait)
            except TimeoutError:
                pass
            except asyncio.CancelledError:
                raise


async def _fake_http_fetch(
    url: str,
    min_delay: float,
    max_delay: float,
    fail_rate: float,
) -> str:
    """模拟网络请求：随机延迟 + 按 fail_rate 概率抛非超时异常。"""
    delay = random.uniform(min_delay, max_delay)
    await asyncio.sleep(delay)
    if random.random() < fail_rate:
        raise RuntimeError(f"network error on {url}")
    return f"<html>{url}</html>"


def _make_default_fetcher(min_delay: float, max_delay: float, fail_rate: float) -> Fetcher:
    async def _fetch(url: str) -> str:
        return await _fake_http_fetch(url, min_delay, max_delay, fail_rate)

    return _fetch


class AsyncRateLimitedCrawler:
    def __init__(
        self,
        *,
        concurrency: int,
        rate: int,
        timeout: float,
        max_retries: int,
        burst: int | None = None,
        min_delay: float = 0.2,
        max_delay: float = 0.8,
        fail_rate: float = 0.2,
        fetcher: Fetcher | None = None,
    ) -> None:
        if concurrency < 1 or rate < 1 or timeout <= 0 or max_retries < 0:
            raise ValueError(
                "concurrency/rate 必须 >= 1，timeout 必须 > 0，max_retries 必须 >= 0"
            )

        self._sem = asyncio.Semaphore(concurrency)
        self._bucket = TokenBucket(rate=float(rate), capacity=burst or max(1, rate))
        self._timeout = timeout
        self._max_retries = max_retries
        self._min_delay = min_delay
        self._max_delay = max_delay
        self._fail_rate = fail_rate
        self._fetcher: Fetcher = fetcher or _make_default_fetcher(
            min_delay, max_delay, fail_rate
        )

        self._cancelled = False
        self._cancel_event = asyncio.Event()
        self._tasks: list[asyncio.Task[CrawlResult]] = []

    async def _request_once(self, task: CrawlTask, attempt: int) -> CrawlResult:
        """单次请求：令牌 + 信号量 + 超时保护，超时返回 TIMEOUT 标记而非抛出。"""
        try:
            async with asyncio.timeout(self._timeout):
                body = await self._fetcher(task.url)
        except TimeoutError:
            return CrawlResult(
                task_id=task.task_id,
                url=task.url,
                status=CrawlStatus.TIMEOUT,
                body=None,
                error="request timeout",
                retries=attempt,
            )
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            return CrawlResult(
                task_id=task.task_id,
                url=task.url,
                status=CrawlStatus.FAILED,
                body=None,
                error=str(exc),
                retries=attempt,
            )

        return CrawlResult(
            task_id=task.task_id,
            url=task.url,
            status=CrawlStatus.SUCCESS,
            body=body,
            error=None,
            retries=attempt,
        )

    async def _crawl_one(self, task: CrawlTask) -> CrawlResult:
        """单个任务的完整生命周期：限速 → 请求 → 失败按指数退避重试，可被优雅取消。"""
        for attempt in range(self._max_retries + 1):
            if self._cancelled:
                return CrawlResult(
                    task_id=task.task_id,
                    url=task.url,
                    status=CrawlStatus.CANCELLED,
                    body=None,
                    error="cancelled",
                    retries=attempt,
                )

            async with self._sem:
                await self._bucket.acquire()
                if self._cancelled:
                    return CrawlResult(
                        task_id=task.task_id,
                        url=task.url,
                        status=CrawlStatus.CANCELLED,
                        body=None,
                        error="cancelled",
                        retries=attempt,
                    )
                result = await self._request_once(task, attempt)

            if result.status != CrawlStatus.FAILED:
                return result

            if attempt < self._max_retries:
                backoff = 0.5 * (2**attempt)
                print(
                    f"[{task.task_id}] ❌ {result.error}，{backoff}s 后第 {attempt + 2} 次重试"
                )
                try:
                    await asyncio.wait_for(self._cancel_event.wait(), timeout=backoff)
                except TimeoutError:
                    continue
                return CrawlResult(
                    task_id=task.task_id,
                    url=task.url,
                    status=CrawlStatus.CANCELLED,
                    body=None,
                    error="cancelled during backoff",
                    retries=attempt + 1,
                )

        return result # type: ignore

    async def crawl(self, tasks: Iterable[CrawlTask]) -> list[CrawlResult]:
        """并发爬取全部任务，返回结构化结果列表；重复调用会重置内部状态。"""
        self._cancelled = False
        self._cancel_event = asyncio.Event()

        task_list = list(tasks)
        self._tasks = [
            asyncio.create_task(self._crawl_one(t), name=f"crawl-{t.task_id}")
            for t in task_list
        ]

        raw = await asyncio.gather(*self._tasks, return_exceptions=True)

        results: list[CrawlResult] = []
        for task, outcome in zip(task_list, raw, strict=True):
            if isinstance(outcome, CrawlResult):
                results.append(outcome)
            elif isinstance(outcome, asyncio.CancelledError):
                results.append(
                    CrawlResult(
                        task_id=task.task_id,
                        url=task.url,
                        status=CrawlStatus.CANCELLED,
                        body=None,
                        error="cancelled",
                        retries=0,
                    )
                )
            else:
                results.append(
                    CrawlResult(
                        task_id=task.task_id,
                        url=task.url,
                        status=CrawlStatus.FAILED,
                        body=None,
                        error=repr(outcome),
                        retries=0,
                    )
                )

        return sorted(results, key=lambda r: r.task_id)

    def cancel(self) -> None:
        """优雅关闭：置取消标记并取消所有未完成任务，已完成的结果原样保留。"""
        self._cancelled = True
        self._cancel_event.set()
        for task in self._tasks:
            if not task.done():
                task.cancel()


def _report(results: list[CrawlResult], label: str) -> None:
    status_counts: dict[CrawlStatus, int] = {}
    for r in results:
        status_counts[r.status] = status_counts.get(r.status, 0) + 1

    print(f"\n=== {label} ===")
    print("状态统计:", ", ".join(f"{s.value}={n}" for s, n in status_counts.items()))

    for r in results:
        match r.status:
            case CrawlStatus.SUCCESS:
                print(f"[{r.task_id}] {r.status.value} retry={r.retries} body={r.body}")
            case CrawlStatus.TIMEOUT:
                print(
                    f"[{r.task_id}] {r.status.value} retry={r.retries} error={r.error}"
                )
            case _:
                print(
                    f"[{r.task_id}] {r.status.value} retry={r.retries} error={r.error}"
                )


async def run_normal() -> None:
    crawler = AsyncRateLimitedCrawler(
        concurrency=3,
        rate=3,
        timeout=1.0,
        max_retries=3,
        min_delay=0.1,
        max_delay=0.5,
        fail_rate=0.3,
    )
    tasks = [CrawlTask(task_id=i, url=f"https://example.com/{i}") for i in range(1, 11)]
    results = await crawler.crawl(tasks)
    _report(results, "完整跑完")


async def run_cancel() -> None:
    crawler = AsyncRateLimitedCrawler(
        concurrency=3,
        rate=3,
        timeout=1.0,
        max_retries=2,
        min_delay=0.3,
        max_delay=1.5,
        fail_rate=0.3,
    )
    tasks = [CrawlTask(task_id=i, url=f"https://example.com/{i}") for i in range(1, 11)]

    crawl_task = asyncio.create_task(crawler.crawl(tasks))

    await asyncio.sleep(3.0)
    print("\n⏰ 外部调用 cancel() 打断……")
    crawler.cancel()

    results = await crawl_task
    _report(results, "中途取消")


async def run() -> None:
    await run_normal()
    await run_cancel()


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
