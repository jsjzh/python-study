# from functools import reduce
from ast import arg
from dataclasses import dataclass
import typing
import numpy as np

# multi_line_string = """

# hello rowld

# king

# """
# print(f"{multi_line_string}")
# print(10 // 3)

# inputType = "count"
# count = input(f"input {inputType}: ")
# count = int(count) if type(count) == "int" else float(count)
# print(count)

# if count > 50:
#     print("> 50")
# else:
#     print("<= 50")

# with open("./index.md", "rb") as f:
#     byteData = f.read()
#     str = byteData.decode(encoding="utf-8", errors="ignore")
#     print(str)
#     print(len(byteData))
#     print(len(str))

# PI = 3.1415926

# print(f"{PI:.2f}")

# s1 = 72
# s2 = 85
# r = (s2 - s1) / s1 * 100
# print(f"{r:.1f}%")
# print("%.1f%%" % r)

# arrs = [1, 2, 3, 4, 5]

# print(
#     f"{arrs[-1]} {arrs.append(6), arrs} {arrs.insert(1, 9), arrs} {arrs.pop(), arrs} {arrs.pop(1), arrs} {arrs}"
# )

# a = ()
# b = 1
# c = [2]
# d = (3,)
# e = (4, 5, 6)

# print(bool([]))

# height = float(input("height(m): "))
# weight = float(input("weight(kg): "))

# print(height)
# print(weight)

# bmi = weight / height / height

# print(bmi)

# if bmi < 18.5:
#     print("过轻")
# elif bmi < 25:
#     print("正常")
# elif bmi < 28:
#     print("过重")
# elif bmi < 32:
#     print("肥胖")
# else:
#     print("严重肥胖")

# age = int(input("age: "))

# match age:
#     case x if x < 10:
#         print(f"hello {x}")
#     case 66 | 88:
#         print("oh")
#     case _:
#         print("world")

# args = [1, 2, 3, 4, 5]

# print(list(map(lambda x: str(x), args)))
# print(reduce(lambda x, y: x + y, args, 0))
# print(sum(args))

# match args:
#     case [1]:
#         print(1)
#     case [1, demo, *demos]:
#         # print(1, demo, "".join(str(e) for e in demos))
#         print(reduce(lambda x, y: (x.append(y), x), demos, [3]))
#     case _:
#         print("no")

# L1 = ["adam", "LISA", "barT"]

# print(list((x * x for x in range(10))))

# print(
#     reduce(
#         lambda x, y: x.append(str(y).capitalize()) or x,
#         map(lambda x: str(x).lower(), L1),
#         [],
#     ),
# )

# print(list(map(lambda x: x.capitalize(), L1)))

# print([name.capitalize() for name in L1])


# print({k.upper(): v for k, v in {"a": 1, "b": 2}.items()})

# print(list(x * x for x in [1, 2, 2, 3] if x > 2))
# print({x * x for x in [1, 2, 2, 3]})


# arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# arr1 = arr[:]
# arr2 = arr[:]
# arr3 = arr[:]
# arr4 = arr[:]

# n = 5
# a = 66
# b = 99
# x = 77

# print(arr[1:4])
# print(arr[:n])
# print(arr[-n:])
# print(arr[::-1])
# print(arr[::2])

# arr1[1:3] = [a, b]
# print("arr1", arr1)

# arr2[1:3] = []
# print("arr2", arr2)

# arr3[0:0] = [x]
# print("arr3", arr3)

# arr4[len(arr4) :] = [x]
# print("arr4", arr4)

# demo = "xxx"

# obj = {"age": 18}

# print(list(obj.keys()))
# print(obj.__hash__)

log = [("user1", 2), ("user2", 7), ("user1", 3), ("user2", 5)]


from typing import Callable, ParamSpec, TypeVar, TypedDict
from functools import partial, reduce

P = ParamSpec("P")
R = TypeVar("R")


def wrap(func: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print("Calling function")
        return func(*args, **kwargs)

    return wrapper


# @wrap
def power(base: float, exp: int) -> float:
    return base**exp


sq = partial(power, exp=3)
sq2 = partial(power, exp=4)

print(sq(10))
print(sq2(10))

# spuare: Partial[power, exp=int] = partial(power, exp=2)
# urls = ["http://example.com"] * 10
# print(urls)

# import threading, requests


# def fetch(url):
#     resp = requests.get(url)
#     print(len(resp.content))


# urls = ["http://example.com"] * 10
# threads = [threading.Thread(target=fetch, args=(u,)) for u in urls]
# for t in threads:
#     t.start()
# for t in threads:
#     t.join()

# logs = [("user1", 2), ("user2", 7), ("user1", 3), ("user2", 5)]

# result = reduce(
#     lambda acc, pair: {**acc, pair[0]: acc.get(pair[0], 0) + pair[1]}, logs, {}
# )

# print(result)


# def show(**kwargs):
#     print(kwargs)


# show(abc=123, hello=321)


logs = [("user1", 2), ("user2", 7), ("user1", 3), ("user2", 5)]

np.append(logs, ("user3", 10))

print(reduce(lambda x, y: {**x, y[0]: x.get(y[0], 0) + y[1]}, logs, {}))

print(1 in [1, 2, 3])

[].copy()


def isDouble(x: int) -> bool:
    return x % 2 == 0


print(isDouble(10.1))


# globalData = 10


# def demo():
#     # global globalData
#     print(globalData)


# print(demo())
# print(globalData)


# def de() -> typing.Dict[str, str | int]:
#     # return (1, 2, 3)
#     # return {1, 2, 3}
#     # return [1, 2, 3]
#     return {"name": "king", "age": 18}


# name, age = de().values()
# print(name, age)


# def show_info(name, age, city):
#     print(f"{name}, {age}, 来自 {city}")


# info1 = {"name": "Alice", "age": 25}
# info2 = {"city": "Beijing"}
# show_info(**info1, **info2)


# class InterfaceResponse(TypedDict):
#     id: int


# def fetch(id: int) -> InterfaceResponse:
#     return {"id": id}


# print(fetch(123).get("id"))


def demo(a, b=178, *args, **kargs):
    print(a)
    print(b)
    print(args)
    print(kargs)


demo(1, 2, 3, 4, 5, 6, name=123, age=321)

try:
    result = 10 / 0
except ZeroDivisionError:
    print("除数不能为0")


@dataclass
class User:
    name: str
    age: int
    email: str


user = User("king", 18, "king@example.com")
print(user)
