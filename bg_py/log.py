from datetime import datetime
from os import getpid
from environment import BG_LOG


def clear_log():
    open(BG_LOG, "w").close()


def write_log(message):
    with open(BG_LOG, "a") as log:
        log.write(f"{datetime.now().replace(microsecond=0)} - {getpid()}: {message}\n")
