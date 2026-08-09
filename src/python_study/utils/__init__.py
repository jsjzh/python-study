import asyncio
from collections.abc import Callable
from contextlib import nullcontext
from dataclasses import dataclass
from enum import Enum
from os import path
import os
import random
import time
from typing import Any, Coroutine

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
def atimer(
    afunc: Callable[..., Coroutine[Any, Any, Any]],
) -> Callable[..., Coroutine[Any, Any, Any]]:

    async def wrapper(*args: Any, **kwargs: Any) -> None:
        start_time = time.perf_counter()
        await afunc(*args, **kwargs)
        end_time = time.perf_counter()

        print(f"\n⏱️ {afunc.__name__} 总耗时：{end_time - start_time:.2f}s")

    return wrapper


def timer(
    fun: Callable[..., Any],
) -> Callable[..., Any]:

    def wrapper(*args: Any, **kwargs: Any) -> None:
        start_time = time.perf_counter()
        fun(*args, **kwargs)
        end_time = time.perf_counter()

        print(f"\n⏱️ {fun.__name__} 总耗时：{end_time - start_time:.2f}s")

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
        except TimeoutError:
            raise TimeoutError(f"[{index}] TimeoutError trigger, >{timeout}s")


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
    index: int, sem: asyncio.Semaphore
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
