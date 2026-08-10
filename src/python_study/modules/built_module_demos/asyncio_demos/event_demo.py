import asyncio
from enum import Enum


async def work(id: int, ready_event: asyncio.Event) -> None:
    print(f"----- [{id}] 等待服务就绪 -----")
    await ready_event.wait()
    print(f"----- [{id}] 开始工作 -----")


async def init(ready_event: asyncio.Event) -> None:
    print(f"----- 初始化中 -----")
    await asyncio.sleep(2)
    print(f"----- 初始化完成 -----")
    ready_event.set()


async def run() -> None:
    ready_event = asyncio.Event()

    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(init(ready_event)),
            *[tg.create_task(work(id, ready_event)) for id in range(1, 11)],
        ]

    print(f"----- 所有 worker 已完成 -----")


class ApprovalStatus(Enum):
    INIT = "init"
    PENDING = "pending"
    APPROVE = "approve"
    REJECT = "reject"
    TIMEOUT = "timeout"


class ApprovalGate(object):
    def __init__(self, action: str) -> None:
        self._action = action
        self._status = ApprovalStatus.INIT
        self._event = asyncio.Event()

    async def request_approval(self, timeout: float | None = None) -> bool:
        if self._status != ApprovalStatus.INIT:
            raise RuntimeError(f"审批已在流程中")

        self._status = ApprovalStatus.PENDING

        try:
            async with asyncio.timeout(timeout):
                await self._event.wait()

                match self._status:
                    case ApprovalStatus.APPROVE:
                        return True
                    case ApprovalStatus.REJECT:
                        return False
                    case _:
                        raise RuntimeError(f"审批状态错误")
        except TimeoutError:
            self._status = ApprovalStatus.TIMEOUT
            self._event.set()
            return False

    def approve(self) -> None:
        if self._status != ApprovalStatus.PENDING:
            raise RuntimeError(f"无法重复审批")

        self._status = ApprovalStatus.APPROVE
        self._event.set()

    def reject(self) -> None:
        if self._status != ApprovalStatus.PENDING:
            raise RuntimeError(f"无法重复审批")

        self._status = ApprovalStatus.REJECT
        self._event.set()


async def run2() -> None:
    ag = ApprovalGate("工作审批")


def main() -> None:
    # asyncio.run(run())
    asyncio.run(run2())
