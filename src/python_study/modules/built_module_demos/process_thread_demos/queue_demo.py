from __future__ import annotations

import multiprocessing
from multiprocessing import Queue


def def_of_child(q: Queue[str]) -> None:
    q.put("hello world from child")


def main() -> None:
    q: Queue[str] = multiprocessing.Queue()

    process = multiprocessing.Process(target=def_of_child, args=(q,))

    process.start()
    process.join()

    msg = q.get()
    print(f"----- parent get msg: {msg} -----")


if __name__ == "__main__":
    main()
