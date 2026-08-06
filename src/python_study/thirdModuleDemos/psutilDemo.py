import psutil


def main() -> None:
    print("----- psutil.cpu_count() -----", psutil.cpu_count())
    print(
        "----- psutil.cpu_count(logical=False) -----", psutil.cpu_count(logical=False)
    )
    print("----- psutil.cpu_times() -----", psutil.cpu_times())

    for x in range(10):
        print(
            "----- psutil.cpu_percent(interval=1, percpu=True) -----",
            psutil.cpu_percent(interval=1, percpu=True),
        )
