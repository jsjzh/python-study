import asyncio


async def unsafe_increment(counter: dict[str, int], name: str) -> None:
    old = counter["value"]
    await asyncio.sleep(0)
    counter["value"] = old + 1
    print(f'----- {name}: {old} -> {counter["value"]} -----')


async def safe_increment(
    counter: dict[str, int], lock: asyncio.Lock, name: str
) -> None:
    async with lock:
        old = counter["value"]
        await asyncio.sleep(0)
        counter["value"] = old + 1
        print(f'----- {name}: {old} -> {counter["value"]} -----')


async def run() -> None:
    counter: dict[str, int] = {"value": 0}
    lock = asyncio.Lock()

    async with asyncio.TaskGroup() as tg:
        for i in range(5):
            tg.create_task(unsafe_increment(counter, f"unsafe{i}"))

    print(f'----- unsafe value {counter["value"]} -----')

    counter["value"] = 0
    async with asyncio.TaskGroup() as tg:
        for i in range(5):
            tg.create_task(safe_increment(counter, lock, f"unsafe{i}"))

    print(f'----- safe value {counter["value"]} -----')


def main() -> None:
    asyncio.run(run())
