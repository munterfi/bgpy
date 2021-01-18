from codecs import encode, decode
from pickle import dumps, loads


def serialize(x: object) -> bytes:
    """
    Serializes a python object.

    Parameters
    ----------
    x : object
        A python object.

    Returns
    -------
    bytes
        Bytes containing the serialized python object
    """
    return encode(dumps(x), "base64")


def deserialize(x: bytes) -> object:
    """
    Deserializes bytes to a python object.

    Parameters
    ----------
    x : bytes
        Bytes containing a serialized python object

    Returns
    -------
    object
        A python object.
    """
    return loads(decode(x, "base64"))
