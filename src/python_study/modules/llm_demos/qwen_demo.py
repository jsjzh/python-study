import asyncio
import json
import os
from typing import TypedDict

import aiohttp
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DASHSCOPE_API_KEY")
workspace_id = "ws-r75qnvqk77br9aj1"

# url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
url = f"https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions"
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}


class Delta(TypedDict):
    content: str


class Choice(TypedDict):
    delta: Delta


class ChatData(TypedDict):
    model: str
    id: str
    choices: list[Choice]
    created: int
    object: str


async def chat_qwen(question: str):
    payload = {
        "model": "qwen-plus",
        "messages": [
            {"role": "system", "content": "你是一个话很少的助手"},
            {"role": "user", "content": question},
            {
                "role": "tool",
                "content": "get_current_time",
                "tool_call_id": "获取时间",
            },
        ],
        "stream": True,
        "stream_options": {"include_usage": True},
        "enable_thinking": False,
    }

    print("----- 正在思考中 -----", question)

    async with aiohttp.ClientSession() as session:
        # print("----- session -----", session)
        async with session.post(url=url, headers=headers, json=payload) as rep:
            # print("----- rep -----", rep)
            async for content in rep.content.iter_any():
                # print("----- content -----", content)
                lines = content.decode("utf-8")
                for line in lines.split("\n"):
                    line = line.strip()
                    # print("----- line -----", line)
                    if line == "data: [DONE]":
                        print("----- 回复结束 -----")
                        return

                    if line and line.startswith("data:"):
                        try:
                            data: ChatData = json.loads(line[5:].strip())
                            if data.get("choices"):
                                message = (
                                    data.get("choices", [{}])[0]
                                    .get("delta", {})
                                    .get("content", "无数据")
                                )
                                print("----- message -----", message or "")
                        except json.JSONDecodeError:
                            pass


def main() -> None:
    asyncio.run(chat_qwen("现在几点了"))
    pass
