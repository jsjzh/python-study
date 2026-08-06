import json
import pickle

from python_study.utils import getAssetsPath


def writeFileWithStr(s: str):
    filePath = getAssetsPath(paths=["index.md"])
    with open(filePath, "a+") as f:
        f.write(f"{s}\n")


def serialize():
    d = {"name": "king", "age": 18}
    filePath = getAssetsPath(paths=["index.md"])
    with open(filePath, "ab") as f:
        f.write(pickle.dumps(d))


def readSerialize():
    filePath = getAssetsPath(paths=["index.md"])
    with open(filePath, "rb") as f:
        print("----- pickle.load(f) -----", pickle.load(f))


def serializeJson():
    filePath = getAssetsPath(paths=["index.md"])
    d = dict(name="金", age=18)
    print("----- d -----", d)
    print("----- type(d) -----", type(d))
    print("----- json.dumps(d) -----", json.dumps(d))
    print("----- type(json.dumps(d)) -----", type(json.dumps(d)))
    with open(filePath, "w") as f:
        f.write(json.dumps(d, ensure_ascii=True))


def readSerializeJson():
    filePath = getAssetsPath(paths=["index.md"])
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


def main():
    writeFileWithStr("hello world")
    # serialize()
    # readSerialize()
    # serializeJson()
    # readSerializeJson()
    # serializeClass()
    pass
