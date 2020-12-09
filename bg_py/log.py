from datetime import datetime
from os import getpid

LOG_FILE = "bg_py.log"


def clear_log():
    open(LOG_FILE, "w").close()


def write_log(message):
    with open(LOG_FILE, "a") as log:
        log.write(f"{datetime.now().replace(microsecond=0)} - {getpid()}: {message}\n")
