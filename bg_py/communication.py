from environment import BG_COMM_FILE, BG_INTERVAL
from datetime import datetime, timedelta
from enum import Enum
from json import dumps, loads
from time import sleep
from typing import Union


class Message(Enum):
    """
    Message types for the communication.

    The message types defined in this enum include:

        - KILL: Never sent as message, triggered by the background process itself.
        - EXIT: Message to tell process to exit.
        - EXECUTE: Message with function call and arguments to execute.
        - OK: Response message, optionally with return values.
        - ERROR: Error message.
    """
    KILL = (0, {})
    EXIT = (1, {})
    EXECUTE = (2, {"command": "", "args": {}})
    OK = (3, {"response": {}})
    ERROR = (4, {"message": "Error occured."})

    def __init__(self, idx, args):
        self.idx = idx

    @property
    def args(self):
        return self.value[1]

    def set_args(self, args):
        self._value_ = (self.idx, args)
        return self

    def args_from_json(self, json):
        return self.set_args(loads(json))

    def args_to_json(self):
        return dumps(self.value[1])


def initialize() -> None:
    """
    Setup file-based communication.
    """
    if _check_communication():
        print("Communcation file already exists.")
    else:
        _clear()


def send_command(command: Message, wait: int = BG_INTERVAL * 2) -> Message:
    """
    Send a command to the background process.

    The command needs to be of type Message.EXECUTE, Message.EXIT or
    Message.KILL. After sending the command, it is waited for a response
    of the background process.

    Parameters
    ----------
    command : Message
        A EXECUTE, EXIT or KILL message with arguments.
    wait : int, optional
        Time to wait for response of the background process,
        by default BG_INTERVAL*2

    Returns
    -------
    Message
        The response from the background process.
    """
    if _check_communication():
        if not _check_command(command):
            return Message.ERROR.set_args(
                {"message": f"Command of invalid message type {command.name}."}
            )
        with open(BG_COMM_FILE, "w") as f:
            f.write(f"{command.name}\n{command.args_to_json()}")
        stop = datetime.now() + timedelta(seconds=wait)
        while datetime.now() < stop:
            response = _receive_response()
            if response is not None:
                break
        else:
            response = Message.ERROR.set_args({"message": "No response received."})
        _clear()
        return response
    else:
        return Message.ERROR.set_args({"message": "Communication not yet initialized."})


def send_response(response: Message) -> Union[None, Message]:
    """
    Sends a response from the background process.

    After a 'send_command' call, the calling process waits for a response from
    the background process. This function is used to respond on the side of the
    background process.

    Parameters
    ----------
    response : Message
        Response message of type OK or ERROR.

    Returns
    -------
    Union[None, Message]
        None if succesfully send response, else an ERROR.
    """
    if _check_communication():
        if not _check_response(response):
            return Message.ERROR.set_args(
                {"message": f"Response of invalid message type {response.name}."}
            )
        with open(BG_COMM_FILE, "w") as f:
            f.write(f"{response.name}\n{response.args_to_json()}")
        sleep(BG_INTERVAL)
        _clear()
    else:
        return Message.ERROR.set_args({"message": "Communication not yet initialized."})


def _receive_response() -> Union[Message, None]:
    if _check_communication():
        if _check_message():
            with open(BG_COMM_FILE, "r") as f:
                lines = f.readlines()
                try:
                    name = lines[0].rstrip("\n")
                    args = lines[1].rstrip("\n")
                except IndexError:
                    return None
            try:
                response = Message[name].args_from_json(args)
            except KeyError:
                response = Message.ERROR.set_args(
                    {"message": f"Unknown response message type {name}."}
                )
            if _check_response(response):
                return response
        else:
            return None
    else:
        return Message.ERROR.set_args({"message": "Communication not yet initialized."})


def receive_command() -> Union[None, Message]:
    """
    Receive a command in the background process.

    In order to make the background process listening to commands, this
    function should be called on a regular basis (e.g. a while loop with sleep
    time 'BG_INTERVAL').

    Returns
    -------
    Union[None, Message]
        Returns None if no command is received or an EXECUTE, EXIT or KILL
        message if a command is received.
    """
    if _check_communication():
        if _check_message():
            with open(BG_COMM_FILE, "r") as f:
                lines = f.readlines()
                try:
                    name = lines[0].rstrip("\n")
                    args = lines[1].rstrip("\n")
                except IndexError:
                    return None
            try:
                command = Message[name].args_from_json(args)
            except KeyError:
                command = Message.KILL.set_args(
                    {"message": f"Unknown command message type {name}."}
                )
            if _check_command(command):
                return command
        else:
            return None
    else:
        return Message.KILL.set_args({"message": "Communication lost."})


def terminate() -> None:
    """
    Terminate file-based communication.

    Removes the communcation file and thereby send KILL message to listening
    background processes.
    """
    if _check_communication():
        BG_COMM_FILE.unlink()
    else:
        print("No communcation file to terminate exists.")


def _clear() -> None:
    open(BG_COMM_FILE, "w").close()


def _check_communication():
    return BG_COMM_FILE.is_file()


def _check_message():
    return BG_COMM_FILE.stat().st_size != 0


def _check_command(message: Message):
    if message in [Message.EXIT, Message.KILL, Message.EXECUTE]:
        return True
    else:
        return False


def _check_response(message: Message):
    if message in [Message.OK, Message.ERROR]:
        return True
    else:
        return False
