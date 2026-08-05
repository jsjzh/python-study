import os
from os import path

base = path.join(os.getcwd(), "src", "python_study")


def _getProjectPath(paths: list[str]) -> str:
    return path.join(base, *paths)


def writeFile():
    filePath = _getProjectPath(paths=["files", "index.md"])
    with open(filePath, "a+") as f:
        f.write("\nhello world")


def main() -> None:
    pass
