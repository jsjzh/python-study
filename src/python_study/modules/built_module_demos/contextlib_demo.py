from contextlib import contextmanager


class Query:
    def __init__(self, name: str) -> None:
        self.name = name

    def query(self) -> None:
        print("----- query -----")


@contextmanager
def create(name: str):
    print("----- create start -----")
    q = Query(name)
    yield q
    print("----- create end -----")


def main() -> None:
    with create("king") as q:
        q.query()
