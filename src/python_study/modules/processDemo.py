from multiprocessing import Pool, Process
import os
import random
import subprocess
import time


def task(index):
    print(f"sub task index: {index} {os.getpid()}")
    startTime = time.time()
    time.sleep(random.random() * 3)
    endTime = time.time()
    print(f"{index} run time {endTime - startTime}")


def processTask():
    print(f"parent process {os.getpid()}")
    p = Process(target=task, args=("processTask",))
    p.start()
    print("waiting...")
    p.join()
    print("waiting done")


def processTasks():
    print(f"parent process {os.getpid()}")
    p = Pool(3)
    for i in range(5):
        p.apply_async(task, args=(i,))
    print("waiting...")
    p.close()
    p.join()
    print("all success")


def subProcessTask():
    print("run subProcessTask")
    result = subprocess.call(["python", "--version"])
    print(f"Exit code: {result}")


# def subProcessTaskCommunicate():
#     print("run subProcessTaskCommunicate")
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
    # processTask()
    # processTasks()
    subProcessTask()
    ## subProcessTaskCommunicate()
    pass
