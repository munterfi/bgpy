from enum import Enum
from json import dumps, loads
from typing import Union, Tuple, TypedDict


class MessageType(Enum):
    """
    Message types for the communication.

    The message types defined in this enum include:

        - INIT:    Only sent once to initialize the background process.
        - EXIT:    Command message to tell process to exit.
        - EXEC: Command message with function call and arguments to execute.
        - OK:      Response message, optionally with return values.
        - ERROR:   Error response message.
    """

    INIT = 0
    EXEC = 1
    EXIT = 2
    OK = 3
    ERROR = 4


class Message:
    """"""

    __slots__ = ["type", "args"]

    def __init__(self, type_: MessageType, args: dict = {}) -> None:
        self.type = type_
        self.args = args

    def __str__(self) -> str:
        return self.type.name

    def get_args(self) -> dict:
        return self.args

    def set_args(self, args: dict) -> None:
        self.args = args
