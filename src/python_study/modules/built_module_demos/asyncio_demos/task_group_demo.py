import asyncio

from python_study.utils import atimer, fake_fetch


@atimer
async def run() -> None:
    sem = asyncio.Semaphore(4)

    try:
        async with asyncio.TaskGroup() as tg:
            tasks = [
                tg.create_task(
                    fake_fetch(index=index, min=0.3, max=2.5, sem=sem, timeout=1)
                )
                for index in range(1, 21)
            ]
    except ExceptionGroup as eg:
        print(f"\n 捕获到 {len(eg.exceptions)} 个异常：")
        for exc in eg.exceptions:
            print(f"{type(exc).__name__}: {exc}")

    results = [
        task.result()
        for task in tasks
        if not task.cancelled() and task.exception() is None
    ]

    print("----- results -----", results)


def main() -> None:
    asyncio.run(run())
