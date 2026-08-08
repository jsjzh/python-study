import asyncio
import statistics
import time

import aiohttp
import requests


async def wait(name: str):
    print("----- start -----", name)
    await asyncio.sleep(1)
    print("----- hello -----", name)
    print("----- end -----", name)


def get_url(id):
    return "https://wireless-devops.souche-inc.com/api/project/getHongmaoZones"


async def request_fetch(id):
    print("----- request_fetch start id -----", id)
    req = requests.get(get_url(id), headers={"_security_token_inc": "91772244355866112"})
    return req.json()


async def request_list():
    ids = [1, 2, 3]
    tasks = [asyncio.create_task(request_fetch(id)) for id in ids]
    return await asyncio.gather(*tasks)


async def aiohttp_fetch(client: aiohttp.ClientSession, id):
    print("----- aiohttp_fetch start id -----", id)
    async with client.get(get_url(id)) as rep:
        return await rep.json()


async def aiohttp_list():
    ids = [1, 2, 3]
    async with aiohttp.ClientSession(
        headers={"_security_token_inc": "91772244355866112"}
    ) as client:
        tasks = [asyncio.create_task(aiohttp_fetch(client, id)) for id in ids]
        return await asyncio.gather(*tasks)


def time_it(fn) -> float:
    start = time.time()
    fn()
    return (time.time() - start) * 1000


def main() -> None:
    rounds = 5
    aiohttp_times: list[float] = []
    request_times: list[float] = []

    for i in range(rounds):
        aiohttp_times.append(time_it(lambda: asyncio.run(aiohttp_list())))
        request_times.append(time_it(lambda: asyncio.run(request_list())))

    aiohttp_median = statistics.median(aiohttp_times)
    request_median = statistics.median(request_times)
    print("----- aiohttp_list times -----", aiohttp_times)
    print(f"----- aiohttp_list median ----- {aiohttp_median:.0f}ms")
    print("----- request_list times -----", request_times)
    print(f"----- request_list median ----- {request_median:.0f}ms")
    print(
        f"----- faster ----- {'aiohttp' if aiohttp_median < request_median else 'requests'}"
    )
