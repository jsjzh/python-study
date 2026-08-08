from datetime import datetime, timedelta


def main():
    print("----- datetime.now() -----", datetime.now())
    print("----- datetime.now().timestamp() -----", datetime.now().timestamp())
    print(
        "----- datetime.fromtimestamp(datetime.now().timestamp()) -----",
        datetime.fromtimestamp(datetime.now().timestamp()),
    )
    print(
        '----- datetime.now().strftime("%Y-%m-%d %H:%M:%S") -----',
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    print(
        "----- datetime.now() + timedelta(hours=-2) -----",
        datetime.now() + timedelta(hours=-2),
    )
