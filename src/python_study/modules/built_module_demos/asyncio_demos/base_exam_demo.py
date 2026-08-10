import asyncio

from python_study.utils import atimer, fake_fetch


@atimer
async def run() -> None:
    sem = asyncio.Semaphore(4)
    results = await asyncio.gather(
        *[
            asyncio.wait_for(fake_fetch(id, sem=sem), timeout=1.2)
            for id in [i for i in range(1, 11)]
        ],
        return_exceptions=True,
    )

    success_count = sum(1 for r in results if isinstance(r, str))
    fail_count = sum(1 for r in results if isinstance(r, Exception))

    print(f"\n📊 汇总: 成功 {success_count} 个, 失败 {fail_count} 个")


def main() -> None:
    asyncio.run(run())
