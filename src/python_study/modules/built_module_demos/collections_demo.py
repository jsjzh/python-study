from collections import ChainMap, OrderedDict, defaultdict, deque
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class LastUpdatedOrderedDict(OrderedDict[int, int]):
    def __init__(self, count: int = 3) -> None:
        super().__init__()
        self._count = count

    def __setitem__(self, key: int, value: int) -> None:
        if key in self:
            super().__setitem__(key, value)
            self.move_to_end(key)
        else:
            if len(self) >= self._count:
                self.popitem(last=False)
            super().__setitem__(key, value)


def main() -> None:
    nt = Point
    print("----- nt -----", nt)
    print("----- nt(123,456) -----", nt(123, 456))
    print("----- type(nt(123, 456)) -----", type(nt(123, 456)))
    print(
        "----- isinstance(nt(123, 456), tuple) -----",
        isinstance(nt(123, 456), tuple),  # type: ignore[reportUnnecessaryIsInstance]
    )

    de = deque(["a", "b", "c"])
    print("----- de -----", de)
    de.append("d")
    print("----- de -----", de)
    de.appendleft("0")
    print("----- de -----", de)

    dd: defaultdict[str, str] = defaultdict(lambda: "no data")
    print('----- dd.get("key", "no") -----', dd.get("key", "no"))
    print('----- dd["key"] -----', dd["key"])

    d = dict([(2, 3), (3, 3), (1, 1)])
    print("----- d -----", d)
    print("----- d.keys() -----", d.keys())
    od = OrderedDict(dict([(2, 3), (3, 3), (1, 1)]))
    print("----- od -----", od)
    print("----- od.keys() -----", od.keys())

    luod = LastUpdatedOrderedDict(count=3)
    luod[0] = 0
    luod[1] = 1
    luod[2] = 2
    print("----- luod -----", luod)
    luod[3] = 3
    print("----- luod -----", luod)

    cd = {"a": "a", "b": "b", "c": "c"}
    ci = {"a": "A", "c": "C"}
    cm = ChainMap(ci, cd)
    print('----- cm["a"] -----', cm["a"])
    print('----- cm["b"] -----', cm["b"])
    print('----- cm["c"] -----', cm["c"])
