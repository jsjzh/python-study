from __future__ import annotations
import multiprocessing

SENTINEL = None


def work(
    task_q: multiprocessing.Queue[int | None],
    result_q: multiprocessing.Queue[int | None],
) -> None:
    while True:
        num = task_q.get()
        if num is SENTINEL:
            result_q.put(SENTINEL)
            break
        else:
            result_q.put(num**2)  # type: ignore


def main() -> None:
    task_q: multiprocessing.Queue[int | None] = multiprocessing.Queue()
    result_q: multiprocessing.Queue[int | None] = multiprocessing.Queue()

    process = multiprocessing.Process(target=work, args=(task_q, result_q))

    process.start()

    for num in range(1, 6):
        task_q.put(num)

    task_q.put(SENTINEL)

    process.join()

    while True:
        try:
            result = result_q.get(timeout=5)
            if result is SENTINEL:
                break
            else:
                print(f"parent get result: {result}")
        except Exception:
            break
