import os
import random
import subprocess
import time
from multiprocessing import Pool, Process


def task(index: int):
    print(f"sub task index: {index} {os.getpid()}")
    start_time = time.time()
    time.sleep(random.random() * 3)
    end_time = time.time()
    print(f"{index} run time {end_time - start_time}")


def process_task():
    print(f"parent process {os.getpid()}")
    p = Process(target=task, args=("process_task",))
    p.start()
    print("waiting...")
    p.join()
    print("waiting done")


def process_tasks():
    print(f"parent process {os.getpid()}")
    p = Pool(3)
    for i in range(5):
        p.apply_async(task, args=(i,))
    print("waiting...")
    p.close()
    p.join()
    print("all success")


def sub_process_task():
    print("run sub_process_task")
    result = subprocess.call(["python", "--version"])
    print(f"Exit code: {result}")


# def sub_process_task_communicate():
#     print("run sub_process_task_communicate")
#     p = subprocess.Popen(
#         ["python"],
#         stdin=subprocess.PIPE,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#     )
#     output, err = p.communicate(b"--version")
#     print("----- output -----", output)
#     print(f"Exit code: {p.returncode}")
#     pass


def main():
    # process_task()
    # process_tasks()
    sub_process_task()
    ## sub_process_task_communicate()
    pass
