from environment import BG_INTERVAL
from log import write_log, clear_log
from communication import _setup, _cleanup, _send_command, _receive_response, Message
from time import sleep
from subprocess import Popen
from sys import executable

process_files = ["background_plain.py", "background_graceful.py", "background_event.py"]

# Choose background process type.
process_files = [process_files[2]]


def main():
    clear_log()
    write_log("Main process: Started")

    _setup()
    write_log("Main process: Communication setup")

    sleep(BG_INTERVAL)
    for process_file in process_files:
        Popen([executable, f"bg_py/{process_file}"])
        sleep(BG_INTERVAL / 3)

    sleep(BG_INTERVAL * 4)
    command = Message.EXECUTE.set_args({"hello": "world"})
    write_log(
        f"Main process: Send command {command.name} with arguments '{command.args_to_json}'"
    )
    response = _send_command(command)
    write_log(
        f"Main process: Received response {response.name} with arguments '{response.args_to_json}'"
    )

    sleep(BG_INTERVAL * 4)
    _cleanup()
    write_log("Main process: Communication stopped")
    write_log("Main process: Ended normally")


if __name__ == "__main__":
    main()