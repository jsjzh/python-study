"""asyncio 进阶：TaskGroup + Semaphore + timeout"""

import asyncio
import random
from collections.abc import Coroutine


async def fake_sse_stream(stream_id: int, sem: asyncio.Semaphore) -> list[str]:
    """模拟一个 SSE 流式响应，受信号量限流"""
    async with sem:
        print(f"[stream-{stream_id}] 🟢 获取到令牌，开始请求")
        chunks: list[str] = []
        try:
            # 模拟网络延迟 0.5~2s
            await asyncio.sleep(random.uniform(0.5, 2.0))
            for i in range(3):
                await asyncio.sleep(0.1)
                chunks.append(f"chunk-{i}")
            print(f"[stream-{stream_id}] ✅ 完成，收到 {len(chunks)} chunks")
        except asyncio.CancelledError:
            print(f"[stream-{stream_id}] ❌ 被取消")
            raise  # ⚠️ 必须重新抛出，否则 TaskGroup 无法感知取消
        return chunks


async def fetch_with_timeout(
    stream_id: int, sem: asyncio.Semaphore, timeout_sec: float
) -> list[str]:
    """给单个任务加超时包装"""
    try:
        async with asyncio.timeout(timeout_sec):
            return await fake_sse_stream(stream_id, sem)
    except TimeoutError:
        print(f"[stream-{stream_id}] ⏰ 超时({timeout_sec}s)，放弃")
        return []


async def start() -> None:
    sem = asyncio.Semaphore(2)  # 🔑 最多 2 个并发，类比 p-limit(2)
    ids = [1, 2, 3, 4, 5]

    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(fetch_with_timeout(i, sem, timeout_sec=1.5)) for i in ids
        ]

    # TaskGroup 退出后，所有任务已完成或异常
    results = [t.result() for t in tasks]
    print(f"\n📊 汇总: {sum(len(r) for r in results)} chunks from {len(ids)} streams")


def main() -> None:
    asyncio.run(start())
