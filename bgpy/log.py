from datetime import datetime
from os import getpid


class Log:
    """
    Logger class
    """

    def __init__(self, log_file: str, location: str, verbose: bool = False) -> None:
        self.log_file = log_file
        self.location = location
        self.verbose = verbose

    def clear(self) -> None:
        """
        Clears the log file.
        """
        open(self.log_file, "w").close()

    def write(self, text: str) -> None:
        """
        Writes text to log file.

        Parameters
        ----------
        text : str
            Log entry text to write.
        """
        formated = self._format(text)
        self._print(formated)
        with open(self.log_file, "a") as f:
            f.write(f"{formated}\n")

    def _print(self, message: str) -> None:
        if self.verbose:
            print(message)

    def _format(self, text: str) -> str:
        return f"{datetime.now().replace(microsecond=0)} - {self.location} {getpid()}: {text}"
