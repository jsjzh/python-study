import requests

url = "https://registry.npmmirror.com/downloads/range/2026-07-30:2026-08-06/clipboard"


def main() -> None:
    r = requests.get(url)
    print("----- r.json() -----", r.json())
    pass
