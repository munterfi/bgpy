from log import write_log, clear_log
from time import sleep
from subprocess import Popen
from sys import executable

process_files = [
    "background_plain.py",
    "background_graceful.py",
    "background_event.py",
]


def main():
    clear_log()
    write_log("Main process: Started")

    sleep(1)
    for process_file in process_files:
        Popen([executable, f"bg_py/{process_file}"])
        sleep(0.5)

    write_log("Main process: Ended normally")


if __name__ == "__main__":
    main()