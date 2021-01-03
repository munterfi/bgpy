from datetime import datetime
from os import getpid
from environment import BG_LOG_FILE


def clear_log() -> None:
    """
    Clears the log file.
    """
    open(BG_LOG_FILE, "w").close()


def write_log(text: str) -> None:
    """
    Writes text to log file.

    Parameters
    ----------
    text : str
        Log entry text to write.
    """
    with open(BG_LOG_FILE, "a") as log:
        log.write(
            f"{datetime.now().replace(microsecond=0)} - {getpid()}: {text}\n"
        )
