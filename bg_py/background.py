from communication import (
    receive_command,
    send_response,
    _receive_initialization,
    Message,
)
from environment import BG_INTERVAL
from log import write_log
from serialize import deserialize
from threading import Event
from sys import argv

BG_ID = argv[1]
exit = Event()


def main():
    write_log("Background process: Started")

    # Initialization message
    write_log("Background process: Waiting for initialization message")
    message = None
    while not exit.is_set() and message is None:
        exit.wait(BG_INTERVAL)
        message = _receive_initialization()
    send_response(
        Message.OK.set_args(
            {"Response": {"bg_id": BG_ID, "message": "f{message.name} OK"}}
        )
    )

    # Check for message of type INIT
    if message is Message.INIT:
        write_log("Background process: Deserialize userdefined loop")
        background_loop = deserialize(message.args["background_loop"])
        init_args = message.args["init_args"]
        write_log("Background process: Entering userdefined loop")
        message = background_loop(exit, init_args)
        write_log("Background process: Left userdefined loop")

    # Check if communication is lost
    if message is Message.KILL:
        write_log(f"Background process: {message.name}, communication lost")

    # Check if exit message was received
    if message is Message.EXIT:
        send_response(Message.OK.set_args({"Response": f"{message.name} OK"}))
        write_log(f"Background process: {message.name}, exit message received.'")
        
    # End background process
    write_log("Background process: Ended")


def quit(signo, _frame):
    write_log(f"Background process: Interrupted by {signo}, shutting down")
    # print("Interrupted by %d, shutting down" % signo)
    exit.set()


if __name__ == "__main__":

    import signal

    # No HUP signal on Windows, crashes ...
    # for sig in ('TERM', 'HUP', 'INT'):
    for sig in ("TERM", "INT"):
        signal.signal(getattr(signal, "SIG" + sig), quit)

    main()
