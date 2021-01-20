from .message import MessageType
from .sockets import ClientSocket, ServerSocket
from .interface import respond  # NOQA


def run(host, port):
    """
    Run a bgpy server.

    Parameters
    ----------
    host : str, optional
        Address of the host where the server runs.
    port : int, optional
        Port where the server is listening.
    """

    INIT = False
    EXIT = False

    with ServerSocket(host, port) as ss:

        while not EXIT:
            sock = ss.accept()

            with ClientSocket(sock=sock) as cs:

                while True:

                    # Read messages
                    msg = cs.recv()
                    if msg is None:
                        break

                    # Message type: INIT
                    if msg.type is MessageType.INIT:
                        if INIT:
                            print("Already initialised.")
                            continue

                        # Extract tasks from INIT message
                        tasks = msg.get_args()
                        init_task = tasks["init_task"]
                        exec_task = tasks["exec_task"]
                        exit_task = tasks["exit_task"]

                        # Execute INIT task and setup init_args
                        init_args = init_task(cs)

                        # Set INIT to True to avoid second initialization
                        INIT = True
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
