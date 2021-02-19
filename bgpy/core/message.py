from enum import Enum


class MessageType(Enum):
    """
    Message types for the messages in the communication.

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
    """
    Messages for the socket communciation.

    Messages to be sent and reveiced via the client sockets. The message
    consists of a message type and arguments. The message type is fixed in the
    communication between the client sockets, and the arguments are used for
    confirmation, error messages and communicating response values.
    """

    __slots__ = ["type", "args"]

    def __init__(self, type_: MessageType, args: dict = {}) -> None:
        self.type = type_
        self.args = args

    def __repr__(self) -> str:
        return f"Message({self.type}, {self.args})"

    def __str__(self) -> str:
        return self.type.name

    def get_args(self) -> dict:
        """
        Get the argument dict of the message.

        Returns
        -------
        dict
            Arguments of the message.
        """
        return self.args

    def set_args(self, args: dict) -> None:
        """
        Set the argument dict of the message.

        Parameters
        ----------
        args : dict
            Arguments to set on the message.

        Returns
        -------
        None
        """
        self.args = args
