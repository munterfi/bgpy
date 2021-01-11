from pickle import dumps, loads
from codecs import encode, decode


def serialize(x):
    return encode(dumps(x), "base64")


def deserialize(x):
    return loads(decode(x, "base64"))
