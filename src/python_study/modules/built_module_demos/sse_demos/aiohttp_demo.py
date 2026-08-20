from __future__ import annotations

import asyncio
import json
import logging
import os
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Any, Literal

import aiohttp
from dacite import Config, from_dict
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY")


logger = logging.getLogger(__name__)


@dataclass
class Delta:
    role: str | None = None
    content: str | None = None
    reasoning_content: str | None = None


@dataclass
class Choice:
    index: int
    delta: Delta


@dataclass
class LLMData:
    id: str
    object: str
    created: int
    model: str
    system_fingerprint: str
    choices: list[Choice]


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
    url = "https://api.deepseek.com/chat/completions"
    data: str = ""
    async for event in aiter_sse(  # type: ignore
        url,
        method="POST",
        headers={
            "Authorization": f"Bearer {API_KEY}",
        },
        data={
            "model": "deepseek-v4-flash",
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个话很少的助手",
                },
                {
                    "role": "user",
                    "content": "你是谁",
                },
            ],
            "thinking": {"type": "enabled"},
            "reasoning_effort": "low",
            "stream": True,
        },
    ):
        try:
            if event.data == "[DONE]":
                return

            payload = from_dict(
                data_class=LLMData,
                data=json.loads(event.data),
                config=Config(strict=False),
            )

            content = payload.choices[0].delta.content

            if content is not None:
                data += content

        except json.JSONDecodeError:
            pass

    print("data", data)


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
