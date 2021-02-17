from .core.environment import STARTUP_TIME, LOG_FILE
from .core.message import Message, MessageType
from .core.sockets import ClientSocket, ServerSocket
from pathlib import Path
from subprocess import Popen
from time import sleep
from typing import Optional


class Server:
    """
    Server to which reveives INIT, EXEC and EXIT from clients, and responds
    with messages of type OK or ERROR.
    """

    __slots__ = ["host", "port", "log_file"]

    def __init__(
        self,
        host: str,
        port: int,
        log_file: Optional[Path] = LOG_FILE,
    ) -> None:
        """
        Initializes a object of type 'Server'.

        Parameters
        ----------
        host : str
            Address of the host to run the server on.
        port : int
            Port where the server will listen.
        log_file : Optional[Path], optional
            Path to the file for writing the logs, by default LOG_FILE.
        """
        self.host = host
        self.port = port
        self.log_file = log_file

    def __str__(self) -> str:
        return (
            "Server with context for running at "
            + f"'{self.host}:{self.port}'"
        )

    def run(self):
        """
        Start the main loop of the server.
        """

        INIT = False
        EXIT = False

        with ServerSocket(self.host, self.port, log_file=self.log_file) as ss:

            while not EXIT:
                sock = ss.accept()

                with ClientSocket(sock=sock, log_file=self.log_file) as cs:

                    while True:

                        # Read messages
                        msg = cs.recv()
                        if msg is None:
                            break

                        # Message type: INIT
                        if msg.type is MessageType.INIT:
                            if INIT:
                                respond(
                                    cs,
                                    {"message": "Already initialized."},
                                    error=True,
                                )
                                continue

                            # Extract tasks from INIT message
                            tasks = msg.get_args()
                            init_task = tasks["init_task"]
                            exec_task = tasks["exec_task"]
                            exit_task = tasks["exit_task"]

                            # Execute INIT task and setup init_args
                            init_args = init_task()

                            # Set INIT to True to avoid second initialization
                            INIT = True

                            # Confirm initialization
                            respond(
                                cs,
                                {"message": "Initialization successful."},
                                error=False,
                            )
                            continue

                        # Message type: EXIT
                        if msg.type is MessageType.EXIT:

                            # Execute exit_task, returns None
                            if INIT:
                                _ = exit_task(cs, init_args, msg.get_args())

                            # Set exit to True and trigger exit
                            EXIT = True
                            break

                        if not INIT:
                            print("Initialize first!")
                            continue

                        # Message type: EXEC
                        if msg.type is MessageType.EXEC:

                            # Execute exec_task and overwrite init_args
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
        _ = Popen(
            [
                "bgpy",
                "server",
                f"{self.host}",
                f"{self.port}",
                f"--log-file={str(self.log_file)}",
            ]
        )
        sleep(STARTUP_TIME)


def respond(
    client_socket: ClientSocket,
    response: dict,
    error: bool = False,
) -> dict:
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
    dict
        Response dict of the client.
    """
    if error:
        msg = Message(MessageType.ERROR, args=response)
    else:
        msg = Message(MessageType.OK, args=response)
    res = client_socket.send(msg)
    return res.get_args()  # type: ignore
