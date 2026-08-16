from __future__ import annotations

import multiprocessing
from dataclasses import dataclass
from queue import Empty

SENTRY = None


@dataclass
class ResultData:
    worker_id: int
    num: int
    result: int


def work(
    worker_id: int,
    task_q: multiprocessing.Queue[int | None],
    result_q: multiprocessing.Queue[ResultData],
) -> None:
    while True:
        num = task_q.get()
        if num is None:
            break
        else:
            result_q.put(ResultData(worker_id=worker_id, num=num, result=num**2))


def main() -> None:
    task_num: int = 10

    task_q: multiprocessing.Queue[int | None] = multiprocessing.Queue()
    result_q: multiprocessing.Queue[ResultData] = multiprocessing.Queue()

    processes = [
        multiprocessing.Process(target=work, args=(worker_id, task_q, result_q))
        for worker_id in range(3)
    ]

    for num in range(1, task_num + 1):
        task_q.put(num)

    for process in processes:
        process.start()

    for _ in processes:
        task_q.put(SENTRY)

    for process in processes:
        process.join()

    results: list[ResultData] = []

    try:
        for _ in range(1, task_num + 1):
            results.append(result_q.get(timeout=5))
    except Empty as exc:
        print(f"----- 接收端超时：{exc} -----")

    for result in results:
        print(f"[worker_id {result.worker_id}] deal {result.num} result {result.result}")


if __name__ == "__main__":
    main()
