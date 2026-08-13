import asyncio
import threading
import time

from python_study.utils import atimer, timer


def download_sync(url: str) -> str:
    time.sleep(0.3)
    return f"content_of_{url}"


@timer
def serial_download(download_count: int = 3) -> None:
    for id in range(download_count):
        download_sync(f"url: {id}")


@timer
def thread_download(download_count: int = 3) -> None:
    threads = [
        threading.Thread(target=download_sync, args=(f"url: {id}",))
        for id in range(download_count)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


@atimer
async def asyncio_download(download_count: int = 3) -> None:
    async with asyncio.TaskGroup() as tg:
        for id in range(download_count):
            tg.create_task(asyncio.to_thread(download_sync, f"url: {id}"))


def main() -> None:
    count = 5

    serial_download(count)
    thread_download(count)
    asyncio.run(asyncio_download(count))


if __name__ == "__main__":
    main()
