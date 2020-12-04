from log import write_log, LOG_FILE
from time import sleep


write_log(LOG_FILE, "Background process: Plain started")

i = 0
while True:
    sleep(2)
    write_log(LOG_FILE, f"Background process: Plain iteration {i}")
    i = i + 1

write_log(LOG_FILE, "Background process: Plain ended normally")


