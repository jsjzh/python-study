import asyncio
import statistics
import time
from collections.abc import Callable

import aiohttp
import requests


async def wait(name: str) -> None:
    print("----- start -----", name)
    await asyncio.sleep(1)
    print("----- hello -----", name)
    print("----- end -----", name)


def get_url(id: int) -> str:
    return "https://wireless-devops.souche-inc.com/api/project/getHongmaoZones"


async def request_fetch(id: int) -> dict[str, object]:
    print("----- request_fetch start id -----", id)
    req = requests.get(get_url(id), headers={"_security_token_inc": "91772244355866112"})
    return req.json()


async def request_list() -> list[dict[str, object]]:
    ids = [1, 2, 3]
    tasks = [asyncio.create_task(request_fetch(id)) for id in ids]
    return await asyncio.gather(*tasks)


async def aiohttp_fetch(client: aiohttp.ClientSession, id: int) -> dict[str, object]:
    print("----- aiohttp_fetch start id -----", id)
    async with client.get(get_url(id)) as rep:
        return await rep.json()


async def aiohttp_list() -> list[dict[str, object]]:
    ids = [1, 2, 3]
    async with aiohttp.ClientSession(
        headers={"_security_token_inc": "91772244355866112"}
    ) as client:
        tasks = [asyncio.create_task(aiohttp_fetch(client, id)) for id in ids]
        return await asyncio.gather(*tasks)


def time_it(fn: Callable[[], object]) -> float:
    start = time.time()
    fn()
    return (time.time() - start) * 1000
