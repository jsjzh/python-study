import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import os
import random


from python_study.utils import atimer, timer


def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


@timer
def serial_judge_prime(nums: list[int]) -> list[bool]:
    """
    执行模型：单线程、单进程、顺序执行。

    主线程: [is_prime(0)] → [is_prime(1)] → ... → [is_prime(19999)]
            ████████████   ████████████          ████████████

    CPU 全程被一个核心占满
    没有任何并发/并行
    """
    return [is_prime(num) for num in nums]


@timer
def thread_judge_prime(nums: list[int]) -> list[bool]:
    """
    执行模型：多线程、单进程、受 GIL 限制。

    线程1: [is_prime(0)]▓▓░░[is_prime(4)]▓▓░░...
    线程2: ░░[is_prime(1)]▓▓░░[is_prime(5)]▓▓...
    线程3: ░░░░[is_prime(2)]▓▓░░[is_prime(6)]...
    ▓▓ = 持有GIL在执行  ░░ = 等待GIL

    submit() 把任务丢进线程池队列，立即返回 Future
    多个线程同时存在，但 CPython GIL 保证同一时刻只有一个线程执行 Python 字节码
    is_prime 是纯 CPU 计算，没有释放 GIL 的 IO 操作 → 线程之间频繁抢锁切换
    结果：比串行还慢（多了线程调度开销），或最多持平
    """
    with ThreadPoolExecutor() as executor:
        exes = [executor.submit(is_prime, num) for num in nums]
    return [exe.result() for exe in exes]


@atimer
async def thread_with_asyncio_judge_prime(nums: list[int]) -> list[bool]:
    """
    执行模型：asyncio 事件循环 + 后台线程池。

    事件循环线程: [提交任务][提交任务]...[await gather 挂起]
                                        ↑ 事件循环空闲，但没有其他协程可调度
    线程池线程1:  [is_prime(0)]▓▓░░[is_prime(N)]▓▓...
    线程池线程2:  ░░[is_prime(1)]▓▓░░[is_prime(N+1)]...

    run_in_executor = "把这个同步函数扔到线程池里跑，返回一个 Future"
    gather 等待所有 Future 完成
    本质上和 thread_judge_prime 一样受 GIL 限制，只是用 asyncio 做了异步编排
    优势不在 CPU 场景，而在混合场景：比如一边发 HTTP 请求一边做计算，事件循环可以在等 IO 时让出控制权
    """
    loop = asyncio.get_running_loop()

    with ThreadPoolExecutor() as executor:
        futures = [loop.run_in_executor(executor, is_prime, num) for num in nums]
        return list(await asyncio.gather(*futures))


@timer
def process_judge_prime(nums: list[int]) -> list[bool]:
    """
    执行模型：多进程、每个进程独立 GIL、真正并行。

    进程1 (独立GIL): [is_prime(0)][is_prime(4)][is_prime(8)]...  ████████████
    进程2 (独立GIL): [is_prime(1)][is_prime(5)][is_prime(9)]...  ████████████
    进程3 (独立GIL): [is_prime(2)][is_prime(6)][is_prime(10)]... ████████████
    进程4 (独立GIL): [is_prime(3)][is_prime(7)][is_prime(11)]... ████████████

    每个子进程有独立的 Python 解释器和内存空间
    submit(is_prime, num) 时：pickle is_prime 的路径 + num → 发送到子进程 → 子进程 unpickle 并执行 → pickle 结果 → 发回父进程
    开销：进程创建 + IPC 序列化/反序列化
    收益：N 核 ≈ N 倍加速（扣除开销后）
    """
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        exes = [executor.submit(is_prime, num) for num in nums]
    return [exe.result() for exe in exes]


@atimer
async def process_with_asyncio_judge_prime(nums: list[int]) -> list[bool]:
    """
    执行模型：asyncio 事件循环 + 后台进程池。

    事件循环线程: [提交][提交]...[await gather 挂起]
                                ↑ 事件循环可以处理其他协程！
    进程1:       [is_prime(0)][is_prime(N)]...  ████████████
    进程2:       [is_prime(1)][is_prime(N+1)]... ████████████

    和 process_judge_prime 的计算能力完全相同（都是多进程真并行）
    区别：事件循环不被阻塞。如果此时还有其他协程在做 IO（比如 SSE 流式接收 LLM 响应），它们可以继续运行
    这是 Agent 开发中最关键的模式：LLM API 调用是 IO 密集，工具执行可能是 CPU 密集，两者需要在同一个事件循环里共存
    """
    loop = asyncio.get_running_loop()

    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = [loop.run_in_executor(executor, is_prime, num) for num in nums]
        return list(await asyncio.gather(*futures))


@atimer
async def asyncio_judge_prime(nums: list[int]) -> list[bool]:
    """
    执行模型：和 thread_with_asyncio_judge_prime 完全等价，只是语法糖。

    asyncio.to_thread(func, *args) = loop.run_in_executor(None, func, *args)
    None 表示使用默认的 ThreadPoolExecutor
    用 TaskGroup 替代 gather：异常安全、结构化并发
    性能上和 #3 一模一样（都是线程池 + GIL），只是写法更现代
    """
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(asyncio.to_thread(is_prime, num)) for num in nums]
    return [task.result() for task in tasks]


def main() -> None:
    """
    | 函数            | 并发模型         | CPU 密集有效？ | 事件循环阻塞？ | Agent 场景适用性 |
    | :-------------- | :--------------- | :------------- | :------------- | :--------------- |
    | serial          | 无               | ✅ 基线        | N/A            | ❌               |
    | thread          | 多线程/GIL       | ❌             | 是             | ❌               |
    | thread+asyncio  | 线程池+事件循环  | ❌             | 否             | ⚠️ 仅 IO         |
    | process         | 多进程           | ✅             | 是             | ⚠️ 纯计算        |
    | process+asyncio | 进程池+事件循环  | ✅             | 否             | ✅ 核心模式      |
    | to_thread       | 线程池+TaskGroup | ❌             | 否             | ✅ IO 工具调用   |
    """

    nums = [random.randint(10**18, 10**19) for _ in range(5)]

    print(f"输入：{nums}\n")

    print(f"结果：{serial_judge_prime(nums)}\n")
    print(f"结果：{thread_judge_prime(nums)}\n")
    print(f"结果：{asyncio.run(thread_with_asyncio_judge_prime(nums))}\n")
    print(f"结果：{process_judge_prime(nums)}\n")
    print(f"结果：{asyncio.run(process_with_asyncio_judge_prime(nums))}\n")
    print(f"结果：{asyncio.run(asyncio_judge_prime(nums))}\n")


if __name__ == "__main__":
    main()
