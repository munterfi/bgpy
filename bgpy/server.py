from .core.environment import STARTUP_TIME, LOG_LEVEL
from .core.log import Log
from .core.message import Message, MessageType
from .core.sockets import ClientSocket, ServerSocket
from .core.token import token_setenv, token_getenv
from importlib import util
from pathlib import Path
from subprocess import Popen
from time import sleep
from typing import Optional


class Server:
    """
    Server to which reveives INIT, EXEC and EXIT messages from clients,
    and responds with messages of type OK or ERROR.
    """

    __slots__ = [
        "host",
        "port",
        "token",
        "log_level",
        "log_file",
        "init_file",
        "log",
    ]

    def __init__(
        self,
        host: str,
        port: int,
        token: Optional[str] = None,
        log_level: str = LOG_LEVEL,
        log_file: Optional[Path] = None,
        init_file: Optional[Path] = None,
    ) -> None:
        """
        Initializes a object of type 'Server'.

        Parameters
        ----------
        host : str
            Address of the host to run the server on.
        port : int
            Port where the server will listen.
        token : str, optional
            Token to check authentification of the client, by default None.
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
        self.token = token
        self.init_file = init_file
        self.log = Log(__name__, log_level, "Server", log_file, True)

    def __repr__(self) -> str:
        return (
            f"Server({self.host!r}, {self.port!r}, "
            + f"{self.log_level!r}, {self.log_file!r},"
            + f"{self.token!r}, {self.init_file!r})"
        )

    def __str__(self) -> str:
        return (
            "Server with context for running at "
            + f"'{self.host}:{self.port}'"
        )

    def run(self):  # noqa: C901
        """
        Start the main loop of the server.
        """

        INIT = False
        EXIT = False
        TOKEN = token_getenv()

        # Initialize from file
        if self.init_file is not None:
            try:
                self.log.info(f"Loading tasks from '{self.init_file}'")
                spec = util.spec_from_file_location(
                    "bgpy.custom.tasks", self.init_file
                )
                tasks = util.module_from_spec(spec)
                spec.loader.exec_module(tasks)
                assert callable(tasks.init_task)
                assert callable(tasks.exec_task)
                assert callable(tasks.exit_task)
                init_task = tasks.init_task
                exec_task = tasks.exec_task
                exit_task = tasks.exit_task
            except Exception as e:
                self.log.exception("Unable to load tasks from file")
                raise e

            # Execute INIT task and setup init_args
            self.log.info("Executing 'init_task'")
            init_args = init_task()

            # Confirm initialization
            self.log.info("Initialization successful")

            # Set INIT to True to avoid second initialization
            INIT = True

        # Start server socket
        with ServerSocket(
            self.host,
            self.port,
            log_level=self.log_level,
            log_file=self.log_file,
        ) as ss:

            if TOKEN is not None:
                self.log.info("Authentication token is set")

            while not EXIT:
                sock = ss.accept()

                # Start serverside client socket
                with ClientSocket(
                    sock=sock,
                    log_level=self.log_level,
                    log_file=self.log_file,
                ) as cs:

                    AUTH = False

                    while True:

                        # Read messages
                        msg = cs.recv()
                        if msg is None:
                            break

                        # Message type: AUTH
                        if msg.type is MessageType.AUTH:
                            token = msg.get_args()["token"]
                            if token == TOKEN or TOKEN is None:

                                # Set AUTH to True to allow further messages
                                AUTH = True

                                # Confirm authentication
                                auth_msg = "Authentication successful"
                                self.log.info(auth_msg)
                                respond(
                                    cs,
                                    {"message": f"{auth_msg}."},
                                    error=False,
                                )
                            else:
                                auth_msg = "Invalid client authentication"
                                self.log.warning(auth_msg)
                                respond(
                                    cs, {"message": f"{auth_msg}."}, error=True
                                )
                            continue

                        if not AUTH:
                            self.log.warning(
                                "Unauthorized access attempt of type "
                                + f"'{msg.type.name}'"
                            )
                            continue

                        # Message type: INIT
                        if msg.type is MessageType.INIT:
                            if INIT:
                                init_msg = "Already initialized"
                                self.log.warning(init_msg)
                                respond(
                                    cs, {"message": f"{init_msg}."}, error=True
                                )
                                continue

                            # Extract tasks from INIT message
                            tasks = msg.get_args()
                            init_task = tasks["init_task"]
                            exec_task = tasks["exec_task"]
                            exit_task = tasks["exit_task"]

                            # Execute INIT task and setup init_args
                            self.log.info("Executing 'init_task'")
                            init_args = init_task()

                            # Set INIT to True to avoid second initialization
                            INIT = True

                            # Confirm initialization
                            init_msg = "Initialization successful"
                            self.log.info(init_msg)
                            respond(
                                cs, {"message": f"{init_msg}."}, error=False
                            )
                            continue

                        # Message type: EXIT
                        if msg.type is MessageType.EXIT:

                            # Execute exit_task, returns None
                            if INIT:
                                self.log.info("Executing 'exit_task'")
                                _ = exit_task(cs, init_args, msg.get_args())

                            # Set exit to True and trigger exit
                            EXIT = True
                            break

                        if not INIT:
                            self.log.warning("Not yet initialized")
                            continue

                        # Message type: EXEC
                        if msg.type is MessageType.EXEC:

                            # Execute exec_task and overwrite init_args
                            self.log.info("Executing 'exec_task'")
                            init_args = exec_task(
                                cs, init_args, msg.get_args()
                            )

    def run_background(self) -> None:
        """
        Run the server in the background.

        Returns
        -------
        Optional[dict]
            Response of the server.
        """
        token_setenv(self.token)
        _ = Popen(
            [
                "bgpy",
                "server",
                f"{self.host}",
                f"{self.port}",
                f"--log-level={str(self.log_level)}",
                f"--log-file={str(self.log_file)}",
                f"--init-file={str(self.init_file)}",
            ]
        )
        sleep(STARTUP_TIME)


def respond(
    client_socket: ClientSocket,
    response: dict,
    error: bool = False,
) -> Optional[Message]:
    """
    Respond to the client

    Send a message OK with custom arguments to the client that initially sent
    a EXEC message. Note: The client has to know that a second response is
    sent by the server and therefore wait for it (await_response=True).

    Parameters
    ----------
    client_socket : ClientSocket
        Client socket, which was set up by the server to handle the
        communication with the client socket on the client.
    response : dict
        Response to send to the client.
    error : bool
        Respond with a Message of type ERROR instead of OK, default is False.

    Returns
    -------
    Optional[Message]
        Response of the client.
    """
    if error:
        msg = Message(MessageType.ERROR, args=response)
    else:
        msg = Message(MessageType.OK, args=response)
    res = client_socket.send(msg)
    return res
