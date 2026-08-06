import asyncio
import time

import aiohttp
import requests


async def wait(name: str):
    print("----- start -----", name)
    await asyncio.sleep(1)
    print("----- hello -----", name)
    print("----- end -----", name)


def getUrl(id):
    return f"https://jsonplaceholder.typicode.com/todos/{id}"


async def requestFetch(id):
    print("----- start id -----", id)
    req = requests.get(getUrl(id))
    return req.json()


async def requestList():
    ids = [1, 2, 3]
    tasks = [asyncio.create_task(requestFetch(id)) for id in ids]
    return await asyncio.gather(*tasks)


async def aiohttpFetch(client, id):
    print("----- start id -----", id)
    async with client.get(getUrl(id)) as rep:
        return await rep.json()


async def aiohttpList():
    ids = [1, 2, 3]
    async with aiohttp.ClientSession() as client:
        tasks = [asyncio.create_task(aiohttpFetch(client, id)) for id in ids]
        return await asyncio.gather(*tasks)


def main() -> None:
    start = time.time()
    datas = asyncio.run(aiohttpList())
    end = time.time()
    times = (end - start) * 1000
    print("----- aiohttpList times -----", times)

    start = time.time()
    datas = asyncio.run(requestList())
    end = time.time()
    times = (end - start) * 1000
    print("----- requestList times -----", times)
