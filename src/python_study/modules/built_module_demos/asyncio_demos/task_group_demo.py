import asyncio
import random

from python_study.utils import atimer, fake_fetch


@atimer
async def run() -> None:
    sem = asyncio.Semaphore(4)
    ids = range(1, 21)

    try:
        async with asyncio.TaskGroup() as tg:
            tasks = [
                tg.create_task(
                    fake_fetch(
                        index=index,
                        min=0.3,
                        max=2.5,
                        timeout=1.0,
                        sem=sem,
                        fail=random.choice(seq=[True, False]),
                    )
                )
                for index in ids
            ]
    except ExceptionGroup as group:
        print(f"----- 异常数：{len(group.exceptions)} -----")
        for exc in group.exceptions:
            print(f"----- 异常名称：{type(exc).__name__} -----")
            print(f"----- 异常内容：{exc} -----")

    results = [
        task.result()
        for task in tasks
        if not task.cancelled() and task.exception() is None
    ]

    success_count = sum(
        [1 for task in tasks if not task.cancelled() and task.exception() is None]
    )

    timeout_count = sum(
        [
            1
            for task in tasks
            if not task.cancelled() and isinstance(task.exception(), TimeoutError)
        ]
    )

    error_count = sum(
        [
            1
            for task in tasks
            if not task.cancelled() and isinstance(task.exception(), Exception)
        ]
    )

    print("----- results -----", results)
    print("----- success_count -----", success_count)
    print("----- timeout_count -----", timeout_count)
    print("----- error_count -----", error_count)


def main() -> None:
    asyncio.run(run())
