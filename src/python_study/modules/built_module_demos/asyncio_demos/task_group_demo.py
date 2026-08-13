import asyncio
from statistics import mean

from python_study.utils import FetchStatus, atimer, safe_fake_fetch


@atimer
async def run() -> None:
    sem = asyncio.Semaphore(4)
    ids = range(1, 21)

    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(safe_fake_fetch(index=index, sem=sem)) for index in ids]

    success_count = sum([1 for task in tasks if task.result().status == FetchStatus.OK])
    timeout_count = sum(
        [1 for task in tasks if task.result().status == FetchStatus.TIMEOUT]
    )
    error_count = sum(
        [1 for task in tasks if task.result().status == FetchStatus.ERROR]
    )
    success_time = [
        task.result().duration
        for task in tasks
        if task.result().status == FetchStatus.OK
    ]
    success_avg_time = mean(success_time) if success_time else 0.0

    print(f"success_count: {success_count}")
    print(f"timeout_count: {timeout_count}")
    print(f"error_count: {error_count}")
    print(f"success_avg_time: {success_avg_time:.2f}s")


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
