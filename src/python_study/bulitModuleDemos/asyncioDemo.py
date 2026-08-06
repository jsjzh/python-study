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


def getUrl(id):
    return "https://wireless-devops.souche-inc.com/api/project/getHongmaoZones"


async def requestFetch(id):
    print("----- requestFetch start id -----", id)
    req = requests.get(getUrl(id), headers={"_security_token_inc": "91772244355866112"})
    return req.json()


async def requestList():
    ids = [1, 2, 3]
    tasks = [asyncio.create_task(requestFetch(id)) for id in ids]
    return await asyncio.gather(*tasks)


async def aiohttpFetch(client: aiohttp.ClientSession, id):
    print("----- aiohttpFetch start id -----", id)
    async with client.get(getUrl(id)) as rep:
        return await rep.json()


async def aiohttpList():
    ids = [1, 2, 3]
    async with aiohttp.ClientSession(
        headers={"_security_token_inc": "91772244355866112"}
    ) as client:
        tasks = [asyncio.create_task(aiohttpFetch(client, id)) for id in ids]
        return await asyncio.gather(*tasks)


def timeIt(fn) -> float:
    start = time.time()
    fn()
    return (time.time() - start) * 1000


def main() -> None:
    rounds = 5
    aiohttpTimes: list[float] = []
    requestTimes: list[float] = []

    for i in range(rounds):
        aiohttpTimes.append(timeIt(lambda: asyncio.run(aiohttpList())))
        requestTimes.append(timeIt(lambda: asyncio.run(requestList())))

    aiohttpMedian = statistics.median(aiohttpTimes)
    requestMedian = statistics.median(requestTimes)
    print("----- aiohttpList times -----", aiohttpTimes)
    print(f"----- aiohttpList median ----- {aiohttpMedian:.0f}ms")
    print("----- requestList times -----", requestTimes)
    print(f"----- requestList median ----- {requestMedian:.0f}ms")
    print(
        f"----- faster ----- {'aiohttp' if aiohttpMedian < requestMedian else 'requests'}"
    )
