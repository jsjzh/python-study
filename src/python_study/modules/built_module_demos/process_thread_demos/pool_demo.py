from __future__ import annotations
import multiprocessing


def square(num: int, extend_msg: int) -> str:
    return f"[extend_msg: {extend_msg}]: {num**2}"


def main() -> None:
    with multiprocessing.Pool(processes=3) as pool:
        results = pool.starmap(square, [(num, num) for num in range(1, 11)])

    for num, result in zip(range(1, 11), results):
        print(f"{num}² = {result}")


if __name__ == "__main__":
    main()
