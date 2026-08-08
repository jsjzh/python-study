from urllib import request

url = "https://registry.npmmirror.com/downloads/range/2026-07-30:2026-08-06/clipboard"


def main() -> None:
    with request.urlopen(url) as f:
        data = f.read()
        print("----- data -----", data)
    pass
