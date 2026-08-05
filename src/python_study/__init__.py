import json
from multiprocessing import Pool, Process
import os
from os import path
import pickle
import random
import re
import subprocess
import time

base = path.join(os.getcwd(), "src", "python_study")


def _getProjectPath(paths: list[str]) -> str:
    return path.join(base, *paths)


def writeFileWithStr(s: str):
    filePath = _getProjectPath(paths=["files", "index.md"])
    with open(filePath, "a+") as f:
        f.write(f"\n{s}")


def serialize():
    d = {"name": "king", "age": 18}
    filePath = _getProjectPath(paths=["files", "index.md"])
    with open(filePath, "ab") as f:
        f.write(pickle.dumps(d))


def readSerialize():
    filePath = _getProjectPath(paths=["files", "index.md"])
    with open(filePath, "rb") as f:
        print("----- pickle.load(f) -----", pickle.load(f))


def serializeJson():
    filePath = _getProjectPath(paths=["files", "index.md"])
    d = dict(name="金", age=18)
    print("----- d -----", d)
    print("----- type(d) -----", type(d))
    print("----- json.dumps(d) -----", json.dumps(d))
    print("----- type(json.dumps(d)) -----", type(json.dumps(d)))
    with open(filePath, "w") as f:
        f.write(json.dumps(d, ensure_ascii=True))


def readSerializeJson():
    filePath = _getProjectPath(paths=["files", "index.md"])
    with open(filePath, "r") as f:
        print("----- json.load(f) -----", json.load(f))


class Student:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


def serializeClass():
    s = Student(name="king", age=18)
    print(
        "----- json.dumps(s, default=lambda obj: obj.__dict__) -----",
        json.dumps(s, default=lambda obj: obj.__dict__),
    )


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


def regDemo():
    print('----- re.match(r"\\d", "1123") -----', re.match(r"^\d+", "1123"))
    print('----- re.split(r"\\s+", "a b c  d e") -----', re.split(r"\s+", "a b c  d e"))
    result = re.match(r"^(\d{4})-(\d{3,8})$", "0570-00000000")
    if result:
        print("----- result.groups() -----", result.groups())
        print("----- result.group(0) -----", result.group(0))
        print("----- result.group(1) -----", result.group(1))
        print("----- result.group(2) -----", result.group(2))
    regPhone = re.compile(r"(^\d{11}$)")
    print(
        "----- regPhone.match('11111111111').groups() -----",
        regPhone.match("11111111111").groups(),
    )


def main() -> None:
    # writeFileWithStr("hello world")
    # serialize()
    # readSerialize()
    # serializeJson()
    # readSerializeJson()
    # serializeClass()
    # processTask()
    # processTasks()
    # subProcessTask()
    ## subProcessTaskCommunicate()
    # regDemo()
    pass
