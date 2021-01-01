from environment import BG_COMM, BG_INTERVAL
from enum import Enum
from os import mkfifo
from time import sleep
from typing import Union


class Command(Enum):
    KILL = 0
    STOP = 1
    RUN = 2


def _setup() -> None:
    if not BG_COMM.is_file():
        _clear()
    else:
        print("Communcation file already exists.")


def _send(command: Command) -> bool:
    if BG_COMM.is_file():
        with open(BG_COMM, "w") as f:
            f.write(f"{command.name}")
        return True
    else:
        print("Communication not yet initialized.")
        return False


def _listen() -> Union[Command, None]:
    if BG_COMM.is_file():
        if BG_COMM.stat().st_size != 0:
            with open(BG_COMM, "r+") as f:
                name = f.read()
            try:
                command = Command[name]
                # Sleep to enable reading by all processes, remove if only one process
                sleep(BG_INTERVAL)
                _clear()
            except KeyError:
                command = Command.KILL
            return command
        else:
            return None
    else:
        return Command.KILL


def _clear() -> None:
    open(BG_COMM, "w").close()


def _cleanup() -> None:
    if BG_COMM.is_file():
        BG_COMM.unlink()
    else:
        print("No communcation file to cleanup exists.")
