from communication import initialize, terminate, send_command, Message
from subprocess import Popen
from log import clear_log  # , write_log
from serialize import serialize
from sys import executable
from pathlib import Path

def start_process(background_loop, init_args: dict) -> Message:
    bg_id = 1
    clear_log()
    initialize()
    print(executable)
    p = Popen([executable, f"{Path(__file__).parent.absolute()}/background.py", f"{bg_id}"])
    response = send_command(
        Message.INIT.set_args({"background_loop": serialize(background_loop),
                               "init_args": init_args})
    )
    return response
