from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import AsyncIterator
from dataclasses import dataclass

import aiohttp
from pydantic import BaseModel, ConfigDict, Field

logger = logging.getLogger(__name__)


class Meta(BaseModel):
    uri: str
    request_id: str
    id: str
    domain: str
    stream: str
    dt: str
    topic: str
    partition: int
    offset: int


class Root(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_info: str = Field(alias="$schema")
    meta: Meta
    id: int | None = None
    type: str
    namespace: int
    title: str
    title_url: str
    comment: str
    timestamp: int
    user: str
    bot: bool
    notify_url: str | None = None
    server_url: str
    server_name: str
    server_script_path: str
    wiki: str
    parsedcomment: str


@dataclass(frozen=True)
class SSEEvent:
    event: str | None
    data: str
    id: str | None


async def iter_sse(
    url: str, *, headers: dict[str, str] | None = None, timeout_sec: float = 30.0
) -> AsyncIterator[SSEEvent]:

    timeout = aiohttp.ClientTimeout(total=timeout_sec)
    async with aiohttp.ClientSession(
        timeout=timeout, proxy="http://127.0.0.1:7897"
    ) as session:
        async with session.get(url, headers=headers) as resp:
            resp.raise_for_status()

            buffer = ""
            async for chunk in resp.content.iter_any():
                buffer += chunk.decode("utf-8")
                while "\n\n" in buffer:
                    raw_event, buffer = buffer.split("\n\n", 1)
                    yield _parse_sse_block(raw_event)


def _parse_sse_block(block: str) -> SSEEvent:
    event_type: str | None = None
    data_lines: list[str] = []
    event_id: str | None = None

    for line in block.split("\n"):
        if line.startswith("event:"):
            event_type = line[6:].strip()
        elif line.startswith("data:"):
            data_lines.append(line[5:].strip())
        elif line.startswith("id:"):
            event_id = line[3:].strip()

    return SSEEvent(event=event_type, data="\n".join(data_lines), id=event_id)


async def run() -> None:
    url = "https://stream.wikimedia.org/v2/stream/recentchange"

    async for event in iter_sse(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        },
    ):
        try:
            payload = Root(**json.loads(event.data))

            logger.info("received title=%s", payload.title)

        except json.JSONDecodeError:
            pass


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
