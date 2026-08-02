import sys


def my_module_hello():
    for item in sys.path:
        print(item)


if __name__ == "__main__":
    my_module_hello()
