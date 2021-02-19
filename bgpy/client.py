from .core.environment import STARTUP_TIME, LOG_LEVEL
from .core.message import Message, MessageType
from .core.sockets import ClientSocket
from time import sleep
from typing import Callable, Optional
from pathlib import Path


class Client:
    """
    Client to send INIT, EXEC and EXIT messages to the the server.
    """

    __slots__ = ["host", "port", "log_level", "log_file"]

    def __init__(
        self,
        host: str,
        port: int,
        log_level: str = LOG_LEVEL,
        log_file: Optional[Path] = None,
    ) -> None:
        """
        Initializes an object of type 'Client'.

        Parameters
        ----------
        host : str
            Address the host where the server runs on.
        port : int
            Port where the server is listening to.
        log_level : str, optional
            The level to log on (DEBUG, INFO, WARNING, ERROR or CRITICAL),
            by default LOG_LEVEL.
        log_file : Optional[Path], optional
            Path to the file for writing the logs, by default None.
        """
        self.host = host
        self.port = port
        self.log_level = log_level
        self.log_file = log_file

    def __repr__(self) -> str:
        return (
            f"Client({self.host!r}, {self.port!r}, "
            + f"{self.log_level!r}, {self.log_file!r})"
        )

    def __str__(self) -> str:
        return (
            "Client context for connecting to server at "
            + f"'{self.host}:{self.port}'"
        )

    def initialize(
        self,
        init_task: Callable,
        exec_task: Callable,
        exit_task: Callable,
    ) -> Optional[dict]:
        """
        Run and intialize a bgpy server on the given host, which starts
        listening to the provided port. After starting the server, a INIT
        message with the 'init_task()', 'exec_task()' and 'exit_task()' tasks
        are send to the server in order to complete the initialization.

        Parameters
        ----------
        init_task : Callable
            Task that runs once during initialization and can be used to set up
            the server. The return value of this function must be a dict, which
            is then passed to the 'exec_task' function with every request of a
            client.
        exec_task : Callable
            Task that is called each time a request is made. Here the message
            from the 'execute' method is interpreted and a task has to be
            defined accordingly. Using the function 'respond' on the server, a
            second response can be sent to the client after the standard
            confirmation of the receipt of the message by the server.
        exit_task : Callable
            Task that is executed once if an exit singal is sent to the server
            by the 'terminate' method. The input of this function is the
            return value of the 'exec_task' function (or if bever called, the
            return value from the 'init_task'). With 'respond' a second message
            can be sent to the client.

        Returns
        -------
        Optional[dict]
            Response of the server.
        """
        with ClientSocket(
            log_level=self.log_level, log_file=self.log_file
        ) as cs:
            cs.connect(self.host, self.port)
            msg = Message(
                MessageType.INIT,
                args={
                    "init_task": init_task,
                    "exec_task": exec_task,
                    "exit_task": exit_task,
                },
            )
            res = cs.send(msg, await_response=True)
            if res is not None:
                return res.get_args()
            else:
                return None

    def execute(
        self,
        exec_args: dict,
        await_response: bool = False,
    ) -> dict:
        """
        Send a command to the server

        Sends an EXEC signal to the server with custom arguments, which are
        passed to the predefined 'exec_task'.

        Parameters
        ----------
        exec_args : dict
            Arguments to send to the 'exec_task'. It is most useful to define a
            command key and a short abbreviation for which the task is checking
            and therefore knows what to do.
        await_response : bool, optional
            Wait for a second 'custom' response of the server, by default
            False.

        Returns
        -------
        dict
            Response of the server.
        """
        with ClientSocket(
            log_level=self.log_level, log_file=self.log_file
        ) as cs:
            cs.connect(self.host, self.port)
            msg = Message(MessageType.EXEC, args=exec_args)
            res = cs.send(msg, await_response=await_response)
            return res.get_args()

    def terminate(
        self,
        exit_args: dict = {},
        await_response: bool = False,
    ) -> dict:
        """
        Terminate the server

        Send an EXIT message to the server in order to execute the 'exit_task'
        and exit the main loop on the server.

        Parameters
        ----------
        exit_args : dict, optional
            Arguments to send to the 'exit_task'.
        await_response : bool, optional
            Wait for a second 'custom' response of the server, by default
            False.

        Returns
        -------
        dict
            Response of the server.
        """
        with ClientSocket(
            log_level=self.log_level, log_file=self.log_file
        ) as cs:
            cs.connect(self.host, self.port)
            msg = Message(MessageType.EXIT, args=exit_args)
            res = cs.send(msg, await_response=await_response)
        sleep(STARTUP_TIME)
        return res.get_args()
