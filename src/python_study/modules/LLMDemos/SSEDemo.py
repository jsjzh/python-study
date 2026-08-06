import asyncio
import json
from typing import TypedDict

import aiohttp

url = "https://stream.wikimedia.org/v2/stream/recentchange"


class Data(TypedDict):
    title: str
    title_url: str
    user: str


async def fetch():
    async with aiohttp.ClientSession(
        proxy="http://127.0.0.1:7897",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        },
    ) as session:
        async with session.get(url=url) as req:
            async for chunk in req.content.iter_any():
                text = chunk.decode("utf-8")
                for line in text.split("\n"):
                    line.strip()
                    if not line or not line.startswith("data:"):
                        continue
                    jsonStr = line[5:].strip()
                    try:
                        data: Data = json.loads(jsonStr)
                        print(
                            '----- data.get("title", "no title") -----',
                            data.get("title", "no title"),
                        )
                    except json.json.JSONDecodeError:
                        pass


def main() -> None:
    print("----- start -----")
    asyncio.run(fetch())
    print("----- end -----")
    pass
