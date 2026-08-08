"""
python_study.modules.bulitModuleDemos.asyncioDemos.semaphoreDemo 的 Docstring

asyncio.Semaphore 控制并发

要用同一个实例，每调用一次，计时器 -1，等到释放后（async with），再 +1，进行下一个等待的任务
"""

import asyncio
import time


async def fakeFetch(index, sem):
    async with sem:
        print(f"start {index}", time.strftime("%H:%M:%S"))
        await asyncio.sleep(1)
        print(f"end {index}", time.strftime("%H:%M:%S"))


async def reStart() -> None:
    sem = asyncio.Semaphore(3)
    tasks = [fakeFetch(i, sem) for i in range(1, 9)]
    await asyncio.gather(*tasks)


def main() -> None:
    asyncio.run(reStart())
