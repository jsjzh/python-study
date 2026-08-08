"""asyncio 核心 API 全家桶 demo：sleep / create_task / cancel / gather / as_completed / wait_for / timeout"""

import asyncio
import time
from collections.abc import Coroutine


def ts() -> str:
    """当前时间戳（秒级），方便观察执行顺序"""
    return time.strftime("%H:%M:%S")


async def fetch(name: str, delay: float) -> str:
    """模拟一个耗时 delay 秒的网络请求"""
    print(f"[{ts()}] {name} 开始")
    await asyncio.sleep(delay)
    print(f"[{ts()}] {name} 完成")
    return f"{name} 的结果"


async def demo_sleep() -> None:
    """① asyncio.sleep：非阻塞等待"""
    print("--- demo_sleep ---")
    print(f"[{ts()}] 开始等 1 秒")
    await asyncio.sleep(1)
    print(f"[{ts()}] 等完了")


async def demo_create_task() -> None:
    """② create_task：立刻调度，实现并发"""
    print("--- demo_create_task ---")
    # 如果直接 await fetch，就是串行（2秒）
    # create_task 让两个任务同时在跑（总共只需 2 秒而不是 3 秒）
    task_a = asyncio.create_task(fetch("A", 2))
    task_b = asyncio.create_task(fetch("B", 1))
    result_a = await task_a
    result_b = await task_b
    print(f"拿到: {result_a}, {result_b}")


async def demo_cancel() -> None:
    """② cancel：手动取消任务"""
    print("--- demo_cancel ---")
    task = asyncio.create_task(fetch("慢任务", 10))
    await asyncio.sleep(0.5)  # 让它跑 0.5 秒
    task.cancel()  # 请求取消
    try:
        await task
    except asyncio.CancelledError:
        print("任务被成功取消")


async def demo_gather() -> None:
    """③ gather：并发执行 + 按顺序收集结果"""
    print("--- demo_gather ---")
    results = await asyncio.gather(
        fetch("G1", 2),
        fetch("G2", 1),
        fetch("G3", 1.5),
    )
    print(f"gather 结果（按传入顺序）: {results}")


async def demo_as_completed() -> None:
    """③ as_completed：谁先完成谁先返回"""
    print("--- demo_as_completed ---")
    coros: list[Coroutine] = [
        fetch("C1", 2),
        fetch("C2", 0.5),
        fetch("C3", 1),
    ]
    for coro in asyncio.as_completed(coros):
        result = await coro
        print(f"  最早完成的先处理: {result}")


async def demo_wait_for() -> None:
    """④ wait_for：给单个协程设超时"""
    print("--- demo_wait_for ---")
    try:
        # 这个请求要 5 秒，但我们只等 1 秒
        result = await asyncio.wait_for(fetch("超时任务", 5), timeout=1.0)
        print(result)
    except TimeoutError:
        print("wait_for 超时，任务已被自动取消")


async def demo_timeout() -> None:
    """④ timeout：给一整块操作设超时（Python 3.11+）"""
    print("--- demo_timeout ---")
    try:
        async with asyncio.timeout(1.5):
            await fetch("步骤1", 1)  # 1 秒，OK
            await fetch("步骤2", 1)  # 累计超过 1.5 秒 → 超时
    except TimeoutError:
        print("timeout 块整体超时")


async def start() -> None:
    await demo_sleep()
    await demo_create_task()
    await demo_cancel()
    await demo_gather()
    await demo_as_completed()
    await demo_wait_for()
    await demo_timeout()


def main() -> None:
    asyncio.run(start())
