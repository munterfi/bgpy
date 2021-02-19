from .environment import (
    LOG_FORMAT,
    LOG_DATETIME_FORMAT,
)
from logging import (
    getLogger,
    Formatter,
    StreamHandler,
    getLevelName,
    DEBUG,
    INFO,
    WARNING,
)
from logging.handlers import RotatingFileHandler
from sys import stdout, stderr
from typing import Optional
from pathlib import Path


class Log:
    """
    Logger class, optionally binds to a log file and writes logs with timestamp
    and PID.
    """

    __slots__ = ["name", "level", "tag", "file", "logger"]

    def __init__(
        self,
        name,
        level: str = "INFO",
        tag: Optional[str] = None,
        file: Optional[Path] = None,
        clear: bool = False,
    ) -> None:
        """
        Initializes an object of type 'Log'.

        Parameters
        ----------
        name : str
            The name of the logger, usually '__name__' is best praxis.
        level : str
            The level to log on (DEBUG, INFO, WARNING, ERROR or CRITICAL).
        tag : str, optional
            Tag of the logging object (e.g. local or remote), by default None.
        file : Path, optional
            Path to the log file, by default None.
        clear : bool, optional
            Clear the provided log file, by default False.
        """

        self.name = name
        self.level = level
        self.tag = tag
        self.file = file

        # Clear log file if exists
        if clear:
            self.clear_log_file()

        # Logger config
        numeric_level = self._level_from_str(level)
        level = level.upper()
        formatter = Formatter(LOG_FORMAT, LOG_DATETIME_FORMAT)
        logger = getLogger(name)
        if logger.hasHandlers():
            logger.debug(self._format("Clear handlers"))
            logger.handlers.clear()
        logger.setLevel(numeric_level)

        # Stream handler
        stream_handler_stdout = StreamHandler(stdout)
        stream_handler_stdout.setFormatter(formatter)
        stream_handler_stdout.setLevel(DEBUG)
        stream_handler_stdout.addFilter(lambda record: record.levelno <= INFO)
        stream_handler_stderr = StreamHandler(stderr)
        stream_handler_stderr.setFormatter(formatter)
        stream_handler_stderr.setLevel(WARNING)
        logger.addHandler(stream_handler_stdout)
        logger.addHandler(stream_handler_stderr)

        # File handler
        if file is not None:
            file_handler = RotatingFileHandler(
                Path(file), maxBytes=512, backupCount=0
            )
            file_handler.setFormatter(formatter)
            file_handler.setLevel(DEBUG)
            logger.addHandler(file_handler)
            logger.debug(
                self._format(
                    f"Set file handler to '{file}'"
                )
            )

        # Complete initialization
        logger.debug(self._format("Set stream handler to 'STDOUT/STDERR'"))
        logger.debug(self._format(f"Set log level to '{level}'"))
        self.logger = logger
        self.logger.debug(self._format("Logger initialized"))

    def __repr__(self) -> str:
        return (
            f"Log({self.name!r}, {self.level!r}, "
            + f"{self.tag!r}, {self.file!r})"
        )

    def __str__(self) -> str:
        return f"Logger {self.name!r} with level {self.level!r}"

    def clear_log_file(self) -> None:
        """
        Clears the log file.
        """
        if self.file is not None:
            open(self.file, "w").close()

    def debug(self, msg: str) -> None:
        """
        Log a message with level "DEBUG"

        Parameters
        ----------
        msg : str
            Message to log.
        """
        self.logger.debug(self._format(msg))

    def info(self, msg: str) -> None:
        """
        Log a message with level "INFO"

        Parameters
        ----------
        msg : str
            Message to log.
        """
        self.logger.info(self._format(msg))

    def warning(self, msg: str) -> None:
        """
        Log a message with level "WARNING"

        Parameters
        ----------
        msg : str
            Message to log.
        """
        self.logger.warning(self._format(msg))

    def error(self, msg: str) -> None:
        """
        Log a message with level "ERROR"

        Parameters
        ----------
        msg : str
            Message to log.
        """
        self.logger.error(self._format(msg))

    def critical(self, msg: str) -> None:
        """
        Log a message with level "CRITICAL"

        Parameters
        ----------
        msg : str
            Message to log.
        """
        self.logger.critical(self._format(msg))

    def exception(self, msg: str) -> None:
        """
        Log an exception with message.

        Parameters
        ----------
        msg : str
            Message to log.
        """
        self.logger.exception(self._format(msg))

    @staticmethod
    def _level_from_str(level_name: str) -> int:
        numeric_level = getLevelName(level_name.upper())
        if not isinstance(numeric_level, int):
            raise ValueError(f"Invalid log level: {level_name}")
        return numeric_level

    def _format(self, msg: str) -> str:
        if self.tag is not None:
            return f"{self.tag} - {msg}"
        else:
            return msg
