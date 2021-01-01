from communication import _listen, Command
from environment import BG_INTERVAL
from log import write_log
from time import sleep

write_log("Background process: Plain started")

i = 0
while True:
    sleep(BG_INTERVAL)
    write_log(f"Background process: Plain iteration {i}")
    
    # Listen to commands
    command = _listen()
    if command is not None:
        write_log(f"Background process: Plain iteration received command: {command.name}")
    if command in [Command.STOP, Command.KILL]:
        break
    
    i = i + 1

# Exit
write_log("Background process: Plain ended gracefully. ")
