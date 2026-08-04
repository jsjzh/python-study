from importlib import resources


def readFile():
    with resources.files("python_study").joinpath("files/index.md").open() as f:
        print(f.read())


def main() -> None:
    readFile()
