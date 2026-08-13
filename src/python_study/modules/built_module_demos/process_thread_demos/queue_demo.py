from __future__ import annotations

from multiprocessing import Queue
import multiprocessing


def def_of_child(q: Queue[str]) -> None:
    q.put("hello world from child")


def main() -> None:
    q: Queue[str] = multiprocessing.Queue()

    process = multiprocessing.Process(target=def_of_child, args=(q,))

    process.start()
    process.join()

    msg = q.get()
    print(f"----- parent get msg: {msg} -----")
