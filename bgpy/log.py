from datetime import datetime
from os import getpid


class Log:
    """
    Logger class, binds to a log file and writes logs with timestamp and PID.
    """

    def __init__(self, log_file: str, tag: str, verbose: bool = False) -> None:
        """
        Initializes a object of type 'Log'.

        Parameters
        ----------
        log_file : str
            Path to the log file.
        tag : str
            tag of the logging object (e.g. local or remote).
        verbose : bool, optional
            Print logs also to the screen, by default True
        """
        self.log_file = log_file
        self.tag = tag
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
        dt = datetime.now().replace(microsecond=0)
        return f"{dt} - {self.tag} {getpid()}: {text}"
