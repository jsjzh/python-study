from __future__ import annotations
import multiprocessing


def square(num: int) -> int:
    return num**2


def main() -> None:
    with multiprocessing.Pool(processes=3) as pool:
        results = pool.map(square, range(1, 11))

    for num, result in zip(range(1, 11), results):
        print(f"{num}² = {result}")


if __name__ == "__main__":
    main()
