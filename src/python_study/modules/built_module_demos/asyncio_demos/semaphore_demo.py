"""
python_study.modules.built_module_demos.asyncio_demos.semaphore_demo 的 Docstring

asyncio.Semaphore 控制并发

要用同一个实例，每调用一次，计时器 -1，等到释放后（async with），再 +1，进行下一个等待的任务
"""

import asyncio

from python_study.utils import fake_fetch


async def re_start() -> None:
    sem = asyncio.Semaphore(3)
    tasks = [fake_fetch(i, sem=sem) for i in range(1, 9)]
    await asyncio.gather(*tasks)


def main() -> None:
    asyncio.run(re_start())


if __name__ == "__main__":
    main()
