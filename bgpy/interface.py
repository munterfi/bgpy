from .environment import BG_HOST, BG_PORT
from .message import Message, MessageType
from .sockets import ClientSocket
from subprocess import Popen
from typing import Callable
from time import sleep


def initialize(
    init_task: Callable,
    exec_task: Callable,
    exit_task: Callable,
    host: str = BG_HOST,
    port: int = BG_PORT,
) -> dict:
    """
    Run and intialize a bgpy server on the given host, which starts listening
    to the provided port. After starting the server, a INIT message with the
    'init_task()', 'exec_task()' and 'exit_task()' tasks are send to the server
    in order to complete the initialization.

    Parameters
    ----------
    init_task : Callable
        Task that runs once during initialization and can be used to set up the
        server. The return value of this function must be a dict, which is then
        given to the 'exec_task' function with with every request.
    exec_task : Callable
        Task that is called each time a request is made. Here the message from
        the 'execute' function has to be interpreted and a task is defined
        accordingly. Using the function 'respond', a second response can be
        sent to the client after the standard confirmation of the receipt of
        the message.
    exit_task : Callable
        Task that is executed once if a exit singal is sent to the server by
        the function 'terminate'. The input of this function is the return
        value of the 'exec_task' function (or if bever called, the return value
        from the 'init_task'). With 'respond' a second message can be sent to
        the client.
    host : str, optional
        Address of the host to run the server on, by default BG_HOST.
    port : int, optional
        Port where the server will listen, by default BG_PORT.

    Returns
    -------
    dict
        Response of the server.
    """
    _ = Popen(["bgpy", "server", f"{host}", f"{port}"])
    sleep(0.5)
    with ClientSocket() as cs:
        cs.connect(host, port)
        msg = Message(
            MessageType.INIT,
            args={
                "init_task": init_task,
                "exec_task": exec_task,
                "exit_task": exit_task,
            },
        )
        res = cs.send(msg)
        return res.get_args()


def execute(
    exec_args: dict,
    await_response: bool = False,
    host: str = BG_HOST,
    port: int = BG_PORT,
) -> dict:
    """
    Send a command to the server

    Sends an EXEC signal to the server with custom arguments, that are passed
    to the predefined 'exec_task'.

    Parameters
    ----------
    exec_args : dict
        Arguments to send to the 'exec_task'. It is most useful to define a
        command key and a short abbreviation for which the task is checking
        and therefore knows what to do.
    await_response : bool, optional
        Wait for a second 'custom' response of the server,
        by default False
    host : str, optional
        Address of the host where the server runs, by default BG_HOST.
    port : int, optional
        Port where the server is listening, by default BG_PORT.

    Returns
    -------
    dict
        Response of the server.
    """
    with ClientSocket() as cs:
        cs.connect(host, port)
        msg = Message(MessageType.EXEC, args=exec_args)
        res = cs.send(msg, await_response=await_response)
        return res.get_args()


def respond(client_socket: ClientSocket, response: dict) -> dict:
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

    Returns
    -------
    dict
        Response of the client.
    """
    msg = Message(MessageType.OK, args=response)
    res = client_socket.send(msg)
    return res.get_args()


def terminate(
    exit_args: dict = {},
    await_response: bool = False,
    host: str = BG_HOST,
    port: int = BG_PORT,
) -> dict:
    """
    Terminate the server

    Send an EXIT message to the server in order to execute the 'exit_task' and
    exit the main loop on the server.

    Parameters
    ----------
    exit_args : dict, optional
        Arguments to send to the 'exit_task'.
    await_response : bool, optional
        Wait for a second 'custom' response of the server,
        by default False
    host : str, optional
        Address of the host where the server runs, by default BG_HOST.
    port : int, optional
        Port where the server is listening, by default BG_PORT.

    Returns
    -------
    dict
        Response of the server.
    """
    with ClientSocket() as cs:
        cs.connect(host, port)
        msg = Message(MessageType.EXIT, args=exit_args)
        res = cs.send(msg, await_response=await_response)
        return res.get_args()
