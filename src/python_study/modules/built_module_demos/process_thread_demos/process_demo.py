import multiprocessing
import os

count: int = 0


def output_pid() -> None:
    global count
    print(f"----- child start count: {count} -----")
    count = 999
    print(f"----- child end count: {count} -----")


def main() -> None:
    global count
    multiprocessing.set_start_method("fork")

    print(f"----- parent start count: {count} -----")

    process = multiprocessing.Process(target=output_pid)
    count = 42
    process.start()
    process.join()

    print(f"----- parent end count: {count} -----")


if __name__ == "__main__":
    main()
