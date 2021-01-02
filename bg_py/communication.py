from environment import BG_COMM, BG_INTERVAL
from enum import Enum
from json import dumps, loads
from time import sleep
from typing import Union


class Command(Enum):
    
    KILL = (1, {})
    STOP = (2, {})
    RUN  = (3, {})
    
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
    if not BG_COMM.is_file():
        _clear()
    else:
        print("Communcation file already exists.")


def _send(command: Command) -> bool:
    if BG_COMM.is_file():
        with open(BG_COMM, "w") as f:
            f.write(f"{command.name}\n{command.args_to_json}")
        return True
    else:
        print("Communication not yet initialized.")
        return False


def _listen() -> Union[Command, None]:
    if BG_COMM.is_file():
        if BG_COMM.stat().st_size != 0:
            with open(BG_COMM, "r+") as f:
                lines = f.readlines()
                name = lines[0].rstrip('\n')
                args = lines[1].rstrip('\n')
            try:
                command = Command[name].args_from_json(args)
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
