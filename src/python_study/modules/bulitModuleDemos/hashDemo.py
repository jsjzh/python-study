import hashlib
import hmac

sb = b"a"


def main():
    print("----- hashlib.md5(sb).hexdigest() -----", hashlib.md5(sb).hexdigest())
    print("----- hashlib.sha1(sb).hexdigest() -----", hashlib.sha1(sb).hexdigest())
    print("----- hashlib.sha224(sb).hexdigest() -----", hashlib.sha224(sb).hexdigest())
    print("----- hashlib.sha256(sb).hexdigest() -----", hashlib.sha256(sb).hexdigest())
    print("----- hashlib.sha384(sb).hexdigest() -----", hashlib.sha384(sb).hexdigest())
    print("----- hashlib.sha512(sb).hexdigest() -----", hashlib.sha512(sb).hexdigest())
    print(
        "----- hashlib.sha3_224(sb).hexdigest() -----", hashlib.sha3_224(sb).hexdigest()
    )
    print(
        "----- hashlib.sha3_256(sb).hexdigest() -----", hashlib.sha3_256(sb).hexdigest()
    )
    print(
        "----- hashlib.sha3_384(sb).hexdigest() -----", hashlib.sha3_384(sb).hexdigest()
    )
    print(
        "----- hashlib.sha3_512(sb).hexdigest() -----", hashlib.sha3_512(sb).hexdigest()
    )
    print(
        "----- hashlib.shake_128(sb).hexdigest() -----",
        hashlib.shake_128(sb).hexdigest(length=10),
    )
    print(
        "----- hashlib.shake_256(sb).hexdigest() -----",
        hashlib.shake_256(sb).hexdigest(length=10),
    )
    print(
        '----- hmac.new(b"new", sb,digestmod="MD5").hexdigest() -----',
        hmac.new(b"new", sb, digestmod="MD5").hexdigest(),
    )
