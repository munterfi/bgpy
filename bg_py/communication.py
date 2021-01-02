from environment import BG_COMM, BG_INTERVAL
from datetime import datetime, timedelta
from enum import Enum
from json import dumps, loads
from time import sleep
from typing import Union


class Message(Enum):

    KILL = (0, {})
    EXIT = (1, {})
    EXECUTE = (2, {"command": "", "args": {}})
    OK = (3, {"response": {}})
    ERROR = (4, {"message": "Error occured."})

    def __init__(self, idx, args):
        self.idx = idx

    def set_args(self, args):
        self._value_ = (self.idx, args)
        return self

    def args_from_json(self, json):
        return self.set_args(loads(json))

    @property
    def args_to_json(self):
        return dumps(self.value[1])


def _setup() -> None:
    if _check_communication():
        print("Communcation file already exists.")
    else:
        _clear()


def _send_command(command: Message, wait: int = BG_INTERVAL * 2):
    if _check_communication():
        if not _check_command(command):
            return Message.ERROR.set_args(
                {"message": f"Command of invalid message type {command.name}."}
            )
        with open(BG_COMM, "w") as f:
            f.write(f"{command.name}\n{command.args_to_json}")
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


def _send_response(response: Message):
    if _check_communication():
        if not _check_response(response):
            return Message.ERROR.set_args(
                {"message": f"Response of invalid message type {response.name}."}
            )
        with open(BG_COMM, "w") as f:
            f.write(f"{response.name}\n{response.args_to_json}")
        sleep(BG_INTERVAL)
        _clear()
    else:
        return Message.ERROR.set_args({"message": "Communication not yet initialized."})


def _receive_response():
    if _check_communication():
        if _check_message():
            with open(BG_COMM, "r") as f:
                lines = f.readlines()
                try:
                    name = lines[0].rstrip("\n")
                    args = lines[1].rstrip("\n")
                except KeyError:
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


def _receive_command():
    if _check_communication():
        if _check_message():
            with open(BG_COMM, "r") as f:
                lines = f.readlines()
                try:
                    name = lines[0].rstrip("\n")
                    args = lines[1].rstrip("\n")
                except KeyError:
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


def _clear() -> None:
    open(BG_COMM, "w").close()


def _cleanup() -> None:
    if _check_communication():
        BG_COMM.unlink()
    else:
        print("No communcation file to cleanup exists.")


def _check_communication():
    return BG_COMM.is_file()


def _check_message():
    return BG_COMM.stat().st_size != 0


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