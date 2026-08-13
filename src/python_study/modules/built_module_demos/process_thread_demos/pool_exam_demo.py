from __future__ import annotations
from dataclasses import dataclass
import hashlib
import multiprocessing
import random
import time

from python_study.utils import timer


def compute_hash(data: str) -> str:
    time.sleep(0.3)
    return f"data: {data} -> hash: {hashlib.md5(data.encode()).hexdigest()[:8]}"


@timer
def pool_map_compute_hash() -> None:
    with multiprocessing.Pool(processes=3) as result:
        results = result.map(
            compute_hash, [f"image_{f'00{id}'[-3:]}" for id in range(1, 11)]
        )

    for result in results:
        print(f"{result}")


@dataclass
class FilterResult:
    name: str
    filter_name: str
    value: float
    output: str


def apply_filter(name: str, filter_name: str, value: float) -> FilterResult:
    time.sleep(0.3)
    return FilterResult(
        name=name,
        filter_name=filter_name,
        value=value,
        output=f"{name}_{filter_name}_{value:.2f}",
    )


@timer
def pool_starmap_apply_filter() -> None:
    with multiprocessing.Pool(processes=3) as pool:
        results = pool.starmap(
            apply_filter,
            [
                (
                    f"image_{f'0{id}'[-2:]}",
                    random.choice(["brightness", "contrast"]),
                    random.uniform(0.5, 1.2),
                )
                for id in range(1, 7)
            ],
        )

    for result in results:
        print(f"{result.output}")


def risky_process(name: str) -> str:
    time.sleep(0.3)
    if random.random() < 0.4:
        raise ValueError(f"process failed for name: {name}")
    return f"ok: {name}"


# TODO
@timer
def pool_apply_async_risky_process() -> None:
    with multiprocessing.Pool() as pool:
        tasks = pool.apply_async(risky_process, args=("123",))

    print(f"tasks.get(): {tasks.get()}")


def main() -> None:
    # pool_map_compute_hash()
    # pool_starmap_apply_filter()
    pool_apply_async_risky_process()


if __name__ == "__main__":
    main()
