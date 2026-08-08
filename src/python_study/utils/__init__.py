from os import path
import os

base = path.join(os.getcwd(), "src", "python_study")


def get_project_path(paths: list[str]) -> str:
    return path.join(base, *paths)


def get_assets_path(paths: list[str]) -> str:
    return path.join(base, "assets", *paths)
