from communication import _receive_command, _send_response, Message
from environment import BG_INTERVAL
from log import write_log
from time import sleep
import signal

write_log("Background process: Graceful started")


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


killer = GracefulKiller()
i = 0
while not killer.kill_now:
    sleep(BG_INTERVAL)
    write_log(f"Background process: Graceful iteration {i}")

    # Listen to commands
    command = _receive_command()
    if command is not None:
        _send_response(Message.OK.set_args({"Response": "Graceful OK"}))
        write_log(
            f"Background process: Graceful iteration received command: {command.name} with arguments '{command.args_to_json}'"
        )
    if command in [Message.EXIT, Message.KILL]:
        break

    i = i + 1

write_log("Background process: Graceful ended normally")
