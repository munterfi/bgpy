from communication import receive_command, send_response, Message
from environment import BG_INTERVAL
from log import write_log
from threading import Event

exit = Event()


def main():
    write_log("Background process: Event started")
    i = 0
    while not exit.is_set():
        exit.wait(BG_INTERVAL)
        write_log(f"Background process: Event iteration {i}")

        # Listen to commands
        command = receive_command()
        if command is not None:
            send_response(Message.OK.set_args({"Response": "Event OK"}))
            write_log(
                f"Background process: Event iteration received command: {command.name} with arguments '{command.args_to_json()}'"
            )
        if command in [Message.EXIT, Message.KILL]:
            break

        i = i + 1

    # Perform any cleanup here
    write_log("Background process: Event ended normally.")


def quit(signo, _frame):
    write_log(f"Background process: Event interrupted by {signo}, shutting down")
    # print("Interrupted by %d, shutting down" % signo)
    exit.set()


if __name__ == "__main__":

    import signal

    # No HUP signal on Windows, crashes ...
    # for sig in ('TERM', 'HUP', 'INT'):
    for sig in ("TERM", "INT"):
        signal.signal(getattr(signal, "SIG" + sig), quit)

    main()
