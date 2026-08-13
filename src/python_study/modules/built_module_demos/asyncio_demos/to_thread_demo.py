import asyncio
import time

from python_study.utils import atimer


def block_io(n: int) -> str:
    time.sleep(1)
    return f"result-{n}"


@atimer
async def run() -> None:
    async with asyncio.TaskGroup() as tg:
        results = [tg.create_task(asyncio.to_thread(block_io, i)) for i in range(1, 4)]

    for result in results:
        print("----- result.result() -----", result.result())


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
