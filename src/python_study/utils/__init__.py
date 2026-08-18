import asyncio
import dataclasses
import datetime
import functools
import json
import logging
import os
import random
import sys
import time
from collections.abc import Callable, Coroutine
from contextlib import nullcontext
from dataclasses import dataclass
from enum import Enum
from os import path
from typing import Any, ParamSpec, TypeVar

base = path.join(os.getcwd(), "src", "python_study")


def get_project_path(paths: list[str]) -> str:
    return path.join(base, *paths)


def get_assets_path(paths: list[str]) -> str:
    return path.join(base, "assets", *paths)


# "一个接收任意参数、返回一个 await 后得到 None 的协程的函数"
# Callable[..., Coroutine[Any, Any, None]]
# Callable[  [...],  Coroutine[Any, Any, None]  ]
#    ↑              ↑
#    参数签名        返回值类型

# 表示"任何可调用对象"
# Callable[[int, str], bool]   # 接收 (int, str)，返回 bool
# Callable[..., bool]          # 接收任意参数，返回 bool
# Callable[[], None]           # 无参，返回 None

# 这是 async def 函数的返回类型
# Coroutine[T_co,   T_contra,      V_co]
#            ↑         ↑            ↑
#     send()的参数 throw()的参数  最终返回值
# 前两个几乎永远是 Any（你不会手动 send/throw）
# 第三个才是你关心的：协程 await 后得到的值

# async def fetch() -> str:       # Coroutine[Any, Any, str]
# async def save() -> None:       # Coroutine[Any, Any, None]
# async def process() -> dict:    # Coroutine[Any, Any, dict[str, Any]]


# Coroutine[Any, Any, None] 可以用 Awaitable[None] 替代

P = ParamSpec("P")
R = TypeVar("R")


def inline_timer(fun_name: str = "") -> Callable[..., None]:
    start = time.perf_counter()

    def end() -> None:
        elapsed = time.perf_counter() - start
        print(f"\n{fun_name} 总耗时：{elapsed:.2f}s\n")

    return end


def atimer[**P, R](
    afunc: Callable[P, Coroutine[Any, Any, R]],
) -> Callable[P, Coroutine[Any, Any, R]]:

    @functools.wraps(afunc)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        result = await afunc(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"\n{afunc.__name__} 总耗时：{elapsed:.2f}s\n")
        return result

    return wrapper


def timer[**P, R](func: Callable[P, R]) -> Callable[P, R]:

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"\n{func.__name__} 总耗时：{end_time - start_time:.2f}s\n")
        return result

    return wrapper


# nullcontext()（空上下文管理器）
# 传了 sem → 拿到的是信号量，async with 会真正做并发限制
# 不传（None） → 拿到的是 nullcontext()，它的 __aenter__/__aexit__ 是空操作，等于没有锁，原样执行
# nullcontext() 是标准库 contextlib 提供的"什么都不做的上下文管理器"，Python 3.10 起支持 async with，所以能直接这样用。这样写的好处就是代码体只写一遍，不用把下载逻辑复制两份
async def fake_fetch(
    index: int,
    min_delay: float = 0.5,
    max_delay: float = 2.0,
    sem: asyncio.Semaphore | None = None,
    fail: bool = False,
    timeout: float | None = None,
) -> str | None:
    async with sem if sem is not None else nullcontext():
        try:
            async with (
                asyncio.timeout(timeout) if timeout is not None else nullcontext()
            ):
                delay = random.uniform(min_delay, max_delay)
                print(f"[{index}] 🟢 开始下载 (delay={delay:.1f}s)")
                await asyncio.sleep(delay)

                if fail:
                    raise ValueError(f"[{index}] valueError trigger")

                print(f"[{index}] ✅ 下载完成")
                return f"data_{index}"
        except TimeoutError as err:
            raise TimeoutError(f"[{index}] TimeoutError trigger, >{timeout}s") from err


class FetchStatus(Enum):
    OK = "ok"
    TIMEOUT = "timeout"
    ERROR = "error"


@dataclass
class FetchResult[T]:
    data: T
    duration: float
    status: FetchStatus = FetchStatus.OK
    message: str | None = None


async def safe_fake_fetch(
    index: int, sem: asyncio.Semaphore | None = None
) -> FetchResult[str | None]:

    start_time = time.perf_counter()

    try:
        result_data = await fake_fetch(
            index=index,
            min_delay=0.3,
            max_delay=2.5,
            sem=sem,
            fail=random.choice([True, False]),
            timeout=1.0,
        )

    except TimeoutError:
        return FetchResult(
            data=None,
            duration=time.perf_counter() - start_time,
            status=FetchStatus.TIMEOUT,
            message=f"{index} timeout error trigger",
        )
    except Exception:
        return FetchResult(
            data=None,
            duration=time.perf_counter() - start_time,
            status=FetchStatus.ERROR,
            message=f"{index} error trigger",
        )

    return FetchResult(
        data=result_data,
        duration=time.perf_counter() - start_time,
    )


def split_string_randomly(s: str, n: int) -> list[str]:
    """
    将一个字符串随机分割成包含 N 个元素的列表。

    Args:
        s: 待分割的原始字符串。
        n: 目标子串数量，必须 >= 1。

    Returns:
        包含 N 个子串的列表，拼接后等于原字符串。

    Raises:
        ValueError: 当 n < 1 或 n > len(s) + 1 时抛出。
    """
    if n < 1:
        raise ValueError(f"n 必须 >= 1，当前值为 {n}")
    if n > len(s) + 1:
        raise ValueError(
            f"n={n} 超出范围，长度为 {len(s)} 的字符串最多可分成 {len(s) + 1} 段"
        )

    # 在 [1, len(s)] 中随机选 n-1 个不重复的切割位置
    cut_points: list[int] = sorted(random.sample(range(1, len(s) + 1), n - 1))

    # 加上首尾边界，依次切片
    boundaries: list[int] = [0, *cut_points, len(s)]
    result: list[str] = [s[boundaries[i] : boundaries[i + 1]] for i in range(n)]

    return result


@dataclass
class StreamData:
    id: int
    name: str
    age: int


fake_data_arr = split_string_randomly(
    json.dumps(
        [
            StreamData(
                id=i,
                name=random.choice(["king", "mm", "gg"]),
                age=random.randint(18, 38),
            )
            for i in range(20)
        ],
        default=lambda obj: dataclasses.asdict(obj),
    ),
    random.randint(20, 30),
)


async def fake_sse_producer(queue: asyncio.Queue[str | None], has_log: bool = False):
    for chunk in fake_data_arr:
        await asyncio.sleep(random.uniform(0.2, 0.5))
        await queue.put(chunk)
        if has_log:
            print(f"----- producer send chunk: {chunk} -----")
    await queue.put(None)


def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def cpu_bound(n: int) -> int:
    """纯 CPU 计算，无 IO"""
    total = 0
    for i in range(n):
        total += i * i
    return total


def wrapper_cpu_bound(nums: list[int]) -> list[tuple[int, int]]:
    return list(zip(nums, [cpu_bound(num) for num in nums], strict=True))


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_entry: dict[str, str | int | float] = {
            "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if record.exc_info is not None:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry, ensure_ascii=False)


def setup_logging(level: int = logging.DEBUG) -> None:
    logger = logging.getLogger("python_study")
    logger.setLevel(level)

    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
    logger.propagate = False
