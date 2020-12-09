from log import write_log, clear_log
from time import sleep
from subprocess import Popen
from sys import executable


def main():
    clear_log()
    write_log("Main process: Started")

    sleep(1)
    Popen([executable, "bg_py/background_plain.py"])
    sleep(1)
    Popen([executable, "bg_py/background_graceful.py"])
    sleep(0.5)
    Popen([executable, "bg_py/background_event.py"])
    sleep(0.5)

    write_log("Main process: Ended normally")


if __name__ == "__main__":
    main()