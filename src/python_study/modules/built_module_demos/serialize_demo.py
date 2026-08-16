import json
import pickle

from python_study.utils import get_assets_path


def write_file_with_str(s: str):
    file_path = get_assets_path(paths=["index.md"])
    with open(file_path, "a+") as f:
        f.write(f"{s}\n")


def serialize():
    d = {"name": "king", "age": 18}
    file_path = get_assets_path(paths=["index.md"])
    with open(file_path, "ab") as f:
        f.write(pickle.dumps(d))


def read_serialize():
    file_path = get_assets_path(paths=["index.md"])
    with open(file_path, "rb") as f:
        print("----- pickle.load(f) -----", pickle.load(f))


def serialize_json():
    file_path = get_assets_path(paths=["index.md"])
    d = dict(name="金", age=18)
    print("----- d -----", d)
    print("----- type(d) -----", type(d))
    print("----- json.dumps(d) -----", json.dumps(d))
    print("----- type(json.dumps(d)) -----", type(json.dumps(d)))
    with open(file_path, "w") as f:
        f.write(json.dumps(d, ensure_ascii=True))


def read_serialize_json():
    file_path = get_assets_path(paths=["index.md"])
    with open(file_path) as f:
        print("----- json.load(f) -----", json.load(f))


class Student:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


def serialize_class():
    s = Student(name="king", age=18)
    print(
        "----- json.dumps(s, default=lambda obj: obj.__dict__) -----",
        json.dumps(s, default=lambda obj: obj.__dict__),
    )


def main():
    write_file_with_str("hello world")
    # serialize()
    # read_serialize()
    # serialize_json()
    # read_serialize_json()
    # serialize_class()
    pass
