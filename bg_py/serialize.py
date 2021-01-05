from pickle import dumps, loads
from codecs import encode, decode


def serialize(x):
    return encode(dumps(x), "base64").decode()


def deserialize(x):
    return loads(decode(x.encode(), "base64"))
