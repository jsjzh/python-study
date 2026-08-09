import asyncio
import json

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


def main() -> None:
    asyncio.run(run())
