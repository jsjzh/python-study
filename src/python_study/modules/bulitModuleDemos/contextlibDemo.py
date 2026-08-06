from contextlib import contextmanager


class Query(object):
    def __init__(self, name):
        self.name = name

    def query(self):
        print("----- query -----")


@contextmanager
def create(name):
    print("----- create start -----")
    q = Query(name)
    yield q
    print("----- create end -----")


def main() -> None:
    with create("king") as q:
        q.query()
