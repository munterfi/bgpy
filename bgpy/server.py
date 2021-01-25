from .message import MessageType
from .sockets import ClientSocket, ServerSocket
from .interface import respond
from pathlib import Path
from typing import Optional


def run(host: str, port: int, log_file: Optional[Path]):
    """
    The bgpy server.

    Start this server vai python using

    Parameters
    ----------
    host : str, optional
        Address of the host where the server runs.
    port : int, optional
        Port where the server is listening.
    log_file : Optional[Path], optional
        Path to the file for writing the logs, by default LOG_FILE.
    """

    INIT = False
    EXIT = False

    with ServerSocket(host, port, log_file=log_file) as ss:

        while not EXIT:
            sock = ss.accept()

            with ClientSocket(sock=sock, log_file=log_file) as cs:

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
                                {"message": "Already initialised."},
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
                        init_args = exec_task(cs, init_args, msg.get_args())
