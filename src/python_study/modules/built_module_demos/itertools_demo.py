import itertools


def get_pi(n: int):
    result = 0
    for c in itertools.takewhile(lambda x: x <= n, itertools.count(1)):
        count = 1 / (c * 2 - 1)
        result += count if c % 2 != 0 else -count
    return result * 4


def main() -> None:
    # for n in itertools.count(0):
    #     print("----- n -----", n)

    # for c in itertools.cycle("HEL"):
    #     print("----- c -----", c)

    # for r in itertools.repeat("A", 3):
    #     print("----- r -----", r)

    # for key, arr in itertools.groupby("Aabcdeabcdee", lambda x: x.upper()):
    #     print("----- key -----", key)
    #     print("----- list(arr) -----", list(arr))

    print("----- get_pi(10) -----", get_pi(10))
    print("----- get_pi(100) -----", get_pi(100))
    print("----- get_pi(1000) -----", get_pi(1000))
    print("----- get_pi(10000) -----", get_pi(10000))
    pass
