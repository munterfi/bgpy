from marshal import dumps, loads
from codecs import encode, decode
from types import FunctionType


def _serialize(x):
    return encode(dumps(x.__code__), "base64").decode()


def _deserialize(x):
    code = loads(decode(x.encode(), "base64"))
    return FunctionType(code, globals())
