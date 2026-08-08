import chardet


def main() -> None:
    print('----- chardet.detect(b"hello") -----', chardet.detect(b"hello"))
    print(
        '----- chardet.detect("我".encode("gbk")) -----',
        chardet.detect("我".encode("gbk")),
    )
    print(
        '----- chardet.detect("最新の主要ニュース".encode("euc-jp")) -----',
        chardet.detect("最新の主要ニュース".encode("euc-jp")),
    )
