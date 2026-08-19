from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Any, Literal

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


class Data(BaseModel):
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


async def aiter_sse(
    url: str,
    proxy: str | None = None,
    method: Literal["GET", "POST"] = "GET",
    data: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    last_event_id: str | None = None,
    max_retries: int = 3,
) -> AsyncIterator[SSEEvent]:
    timeout = aiohttp.ClientTimeout(connect=5.0, sock_read=60.0, total=300.0)

    merged_headers = {**(headers or {})}
    if last_event_id is not None:
        merged_headers["Last-Event-ID"] = last_event_id

    async with aiohttp.ClientSession(timeout=timeout, proxy=proxy) as session:
        for current_count in range(1, max_retries + 1):
            try:
                async with session.request(
                    method=method,
                    url=url,
                    params=data if method == "GET" else None,
                    json=data if method == "POST" else None,
                    headers=merged_headers,
                ) as resp:
                    resp.raise_for_status()
                    buffer = ""
                    async for chunk in resp.content.iter_any():
                        buffer += chunk.decode("utf-8")
                        while "\n\n" in buffer:
                            raw_event, buffer = buffer.split("\n\n", 1)
                            yield _parse_sse_block(raw_event)
            except (
                aiohttp.ClientConnectionError,
                aiohttp.ClientResponseError,
            ) as err:
                if isinstance(err, aiohttp.ClientConnectionError) or (
                    500 <= err.status < 600
                ):
                    if current_count < max_retries + 1:
                        wait_time = 0.5 * 2 ** (current_count - 1)
                        await asyncio.sleep(wait_time)
                        logger.warning(
                            "将在 %.1f 秒后进行第 %d 次重试",
                            wait_time,
                            current_count,
                        )
                        continue
                    raise err
                else:
                    raise err


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

    async for event in aiter_sse(
        url,
        method="GET",
        proxy="http://127.0.0.1:7897",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        },
    ):
        try:
            payload = Data(**json.loads(event.data))

            logger.info("received title=%s", payload.title)

        except json.JSONDecodeError:
            pass


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
