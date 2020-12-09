from log import write_log
from time import sleep


write_log("Background process: Plain started")

i = 0
while True:
    sleep(2)
    write_log(f"Background process: Plain iteration {i}")
    i = i + 1

# Never happens...
write_log("Background process: Plain ended gracefully. ")
