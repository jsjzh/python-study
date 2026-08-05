import subprocess
import sys
import threading
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

SRC_DIR = Path(__file__).resolve().parent.parent
WATCH_GLOBS = ("*.py",)
DEBOUNCE_SECONDS = 0.5


class ReloadHandler(FileSystemEventHandler):
    def __init__(self) -> None:
        self._timer: threading.Timer | None = None
        self._lock = threading.Lock()

    def on_any_event(self, event) -> None:
        if event.is_directory:
            return
        if not event.src_path.endswith(".py"):
            return
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
            self._timer = threading.Timer(DEBOUNCE_SECONDS, self._run)
            self._timer.daemon = True
            self._timer.start()

    def _run(self) -> None:
        print("\x1b[2J\x1b[H", end="", flush=True)
        print("[dev] change detected, restarting `uv run start`...\n", flush=True)
        subprocess.run(["uv", "run", "start"])


def main() -> None:
    handler = ReloadHandler()
    observer = Observer()
    observer.schedule(handler, str(SRC_DIR), recursive=True)
    observer.start()
    print(f"[dev] watching {SRC_DIR} (Ctrl+C to stop)\n", flush=True)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    sys.exit(main())
