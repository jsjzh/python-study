from __future__ import annotations
import multiprocessing
import threading

from python_study.utils import timer, wrapper_cpu_bound

nums = [10_000_00 for _ in range(20)]


@timer
def bench_sequential() -> None:
    wrapper_cpu_bound(nums)
    wrapper_cpu_bound(nums)


@timer
def bench_threading() -> None:
    t1 = threading.Thread(target=wrapper_cpu_bound, args=(nums,))
    t2 = threading.Thread(target=wrapper_cpu_bound, args=(nums,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


@timer
def bench_multiprocessing() -> None:
    with multiprocessing.Pool(2) as pool:
        pool.map(wrapper_cpu_bound, [nums, nums])


def main() -> None:
    bench_sequential()
    bench_threading()
    bench_multiprocessing()


if __name__ == "__main__":
    main()
