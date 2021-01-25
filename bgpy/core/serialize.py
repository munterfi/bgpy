from .message import Message
from codecs import encode, decode
from pickle import dumps, loads


def serialize(x: Message) -> bytes:
    """
    Serializes a Python Message object.

    Parameters
    ----------
    x : object
        A Python Message object.

    Returns
    -------
    bytes
        Bytes containing the serialized Python Message object.
    """
    return encode(dumps(x), "base64")


def deserialize(x: bytes) -> Message:
    """
    Deserializes bytes to a Python Message object.

    Parameters
    ----------
    x : bytes
        Bytes containing a serialized Python Message object.

    Returns
    -------
    object
        A python object.
    """
    return loads(decode(x, "base64"))
