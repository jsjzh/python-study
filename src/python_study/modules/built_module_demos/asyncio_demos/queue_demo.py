import asyncio
import json
from enum import Enum

from python_study.utils import StreamData, fake_sse_producer


async def sse_consumer(
    sse_q: asyncio.Queue[str | None],
    result_q: asyncio.Queue[StreamData | None],
) -> None:
    data: str = ""
    while True:
        chunk = await sse_q.get()
        if chunk is None:
            results = json.loads(data)
            print(f"----- sse_consumer done {results} -----")
            for item in results:
                await result_q.put(StreamData(**item))
                await result_q.put(None)
        else:
            data += chunk


async def result_consumer(result_q: asyncio.Queue[StreamData | None]) -> None:
    while True:
        item = await result_q.get()
        if item is not None:
            print(f"----- id: {item.id}, name: {item.name}, age: {item.age} -----")


async def run():
    sse_q: asyncio.Queue[str | None] = asyncio.Queue()
    result_q: asyncio.Queue[StreamData | None] = asyncio.Queue()

    async with asyncio.TaskGroup() as tg:
        tg.create_task(fake_sse_producer(sse_q, has_log=True))
        tg.create_task(sse_consumer(sse_q, result_q))
        tg.create_task(result_consumer(result_q))


class MessageStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    STOPPED = "stopped"


class MessageProcessor:
    def __init__(self, maxsize: int = 10) -> None:
        self._maxsize: int = maxsize
        self._q: asyncio.Queue = asyncio.Queue(maxsize=maxsize)
        self._status: MessageStatus = MessageStatus.IDLE
        self._tasks: list[asyncio.Task[None]] = []
        self._worker_count: int = 0

    async def _worker(self, work_id: int) -> None:
        while True:
            try:
                msg = await self._q.get()
                if msg is not None:
                    await asyncio.sleep(0.1)
                    print(f"----- [w-{work_id}] 处理 {msg} -----")
                else:
                    break
            except Exception as error:
                raise RuntimeError("worker error") from error
            finally:
                self._q.task_done()

    async def start(self, workers: int = 2) -> None:
        if self._status == MessageStatus.RUNNING:
            raise RuntimeError("流程无法重复开始")

        self._status = MessageStatus.RUNNING
        self._worker_count = workers

        for worker in range(workers):
            task = asyncio.create_task(self._worker(worker))
            self._tasks.append(task)

    async def submit(self, message: str) -> None:
        if self._status == MessageStatus.IDLE:
            raise RuntimeError("流程未启动，无法 submit")
        if self._status == MessageStatus.STOPPED:
            raise RuntimeError("流程暂停，无法 submit")

        await self._q.put(message)

    async def stop(self) -> None:
        if self._status == MessageStatus.IDLE:
            raise RuntimeError("流程未启动")
        if self._status == MessageStatus.STOPPED:
            raise RuntimeError("流程无法重复暂停")

        for _ in range(self._worker_count):
            await self._q.put(None)

        await self._q.join()

        self._status = MessageStatus.STOPPED


async def run2() -> None:
    MessageProcessor(maxsize=5)


def main() -> None:
    # asyncio.run(run())
    asyncio.run(run2())


if __name__ == "__main__":
    main()
