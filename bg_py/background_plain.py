from communication import receive_command, send_response, Message
from environment import BG_INTERVAL
from log import write_log
from time import sleep

write_log("Background process: Plain started")

i = 0
while True:
    sleep(BG_INTERVAL)
    write_log(f"Background process: Plain iteration {i}")

    # Listen to commands
    command = receive_command()
    if command is not None:
        send_response(Message.OK.set_args({"Response": "Plain OK"}))
        write_log(
            f"Background process: Plain iteration received command: {command.name} with arguments '{command.args_to_json}'"
        )
    if command in [Message.EXIT, Message.KILL]:
        break

    i = i + 1

# Exit
write_log("Background process: Plain ended normally. ")
