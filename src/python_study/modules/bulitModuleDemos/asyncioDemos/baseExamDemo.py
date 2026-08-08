import asyncio
import random
import time
from collections.abc import Awaitable, Callable, Coroutine
from typing import Any

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
    afunc: Callable[..., Coroutine[Any, Any, None]],
) -> Callable[..., Coroutine[Any, Any, None]]:

    async def wrapper(*args: Any, **kargs: Any) -> None:
        start_time = time.perf_counter()
        await afunc(*args, **kargs)
        end_time = time.perf_counter()

        print(f"\n⏱️ {afunc.__name__} 总耗时：{end_time - start_time:.2f}s")

    return wrapper


async def fake_fetch(index: int, sem: asyncio.Semaphore) -> str | None:
    async with sem:
        delay = random.uniform(0.5, 2.0)
        print(f"[{index}] 🟢 开始下载 (delay={delay:.1f}s)")
        await asyncio.sleep(delay)
        print(f"[{index}] ✅ 下载完成")
        return f"data_{index}"


@atimer
async def run() -> None:
    sem = asyncio.Semaphore(4)
    results = await asyncio.gather(
        *[
            asyncio.wait_for(fake_fetch(id, sem), timeout=1.2)
            for id in [i for i in range(1, 11)]
        ],
        return_exceptions=True,
    )

    success_count = sum(1 for r in results if isinstance(r, str))
    fail_count = sum(1 for r in results if isinstance(r, Exception))

    print(f"\n📊 汇总: 成功 {success_count} 个, 失败 {fail_count} 个")


def main() -> None:
    asyncio.run(run())
