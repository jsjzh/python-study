"""对比三种并发模型处理 CPU 密集 vs IO 密集任务的性能差异"""

import asyncio
import threading
import multiprocessing
import time


# ---------- CPU 密集任务：计算大量平方 ----------
def cpu_heavy(n: int) -> int:
    total = 0
    for i in range(n):
        total += i * i
    return total


# ---------- IO 密集任务：模拟网络请求 ----------
async def io_heavy(url: str) -> str:
    await asyncio.sleep(0.5)  # 模拟网络延迟
    return f"response from {url}"


# ========== 1. 串行基线 ==========
def run_serial_cpu() -> None:
    start = time.perf_counter()
    for _ in range(4):
        cpu_heavy(5_000_000)
    print(f"[serial CPU]      {time.perf_counter() - start:.3f}s")


# ========== 2. threading（CPU 密集 → 受 GIL 限制） ==========
def run_thread_cpu() -> None:
    start = time.perf_counter()
    threads = [threading.Thread(target=cpu_heavy, args=(5_000_000,)) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"[threading CPU]   {time.perf_counter() - start:.3f}s")


# ========== 3. multiprocessing（CPU 密集 → 绕开 GIL） ==========
def run_process_cpu() -> None:
    start = time.perf_counter()
    procs = [
        multiprocessing.Process(target=cpu_heavy, args=(5_000_000,)) for _ in range(4)
    ]
    for p in procs:
        p.start()
    for p in procs:
        p.join()
    print(f"[multiproc CPU]   {time.perf_counter() - start:.3f}s")


# ========== 4. asyncio（IO 密集 → 最佳选择） ==========
async def run_asyncio_io() -> None:
    start = time.perf_counter()
    tasks = [io_heavy(f"url_{i}") for i in range(4)]
    await asyncio.gather(*tasks)
    print(f"[asyncio IO]      {time.perf_counter() - start:.3f}s")


# ========== 5. threading（IO 密集 → 也能用） ==========
def io_sync(url: str) -> str:
    time.sleep(0.5)
    return f"response from {url}"


def run_thread_io() -> None:
    start = time.perf_counter()
    threads = [threading.Thread(target=io_sync, args=(f"url_{i}",)) for i in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"[threading IO]    {time.perf_counter() - start:.3f}s")


def main() -> None:
    run_serial_cpu()
    run_thread_cpu()
    run_process_cpu()
    asyncio.run(run_asyncio_io())
    run_thread_io()


if __name__ == "__main__":
    main()
