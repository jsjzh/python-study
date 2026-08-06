from os import path
import os

base = path.join(os.getcwd(), "src", "python_study")


def getProjectPath(paths: list[str]) -> str:
    return path.join(base, *paths)


def getAssetsPath(paths: list[str]) -> str:
    return path.join(base, "assets", *paths)
