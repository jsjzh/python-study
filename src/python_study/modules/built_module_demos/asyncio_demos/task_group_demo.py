import asyncio

from python_study.utils import atimer, fake_fetch


@atimer
async def run() -> None:
    ids = range(1, 11)

    try:
        async with asyncio.TaskGroup() as tg:
            tasks = [
                tg.create_task(asyncio.wait_for(fake_fetch(id), timeout=1))
                for id in ids
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
