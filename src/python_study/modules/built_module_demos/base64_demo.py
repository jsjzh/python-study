import base64


def main():
    print('----- base64.b64encode(b"hello world") -----', base64.b64encode(b"hello world"))
    print(
        "----- base64.b64decode(b'aGVsbG8gd29ybGQ=') -----",
        base64.b64decode(b"aGVsbG8gd29ybGQ="),
    )
    print(
        '----- base64.b64decode(b"aGVsbG8gd29ybGQ=").decode() -----',
        base64.b64decode(b"aGVsbG8gd29ybGQ=").decode(),
    )
