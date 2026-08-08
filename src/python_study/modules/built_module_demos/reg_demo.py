import re


def main():
    print('----- re.match(r"\\d", "1123") -----', re.match(r"^\d+", "1123"))
    print('----- re.split(r"\\s+", "a b c  d e") -----', re.split(r"\s+", "a b c  d e"))
    result = re.match(r"^(\d{4})-(\d{3,8})$", "0570-00000000")
    if result:
        print("----- result.groups() -----", result.groups())
        print("----- result.group(0) -----", result.group(0))
        print("----- result.group(1) -----", result.group(1))
        print("----- result.group(2) -----", result.group(2))
    reg_phone = re.compile(r"(^\d{11}$)")
    print(
        "----- reg_phone.match('11111111111').groups() -----",
        reg_phone.match("11111111111").groups(),
    )
