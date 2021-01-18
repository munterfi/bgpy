from environment import BG_HOST, BG_PORT
from message import Message, MessageType
from sockets import ClientSocket
from subprocess import Popen
from sys import executable
from pathlib import Path


def initialize(
    init_task, exec_task, exit_task, host: str = BG_HOST, port: int = BG_PORT
):
    _ = Popen(
        [
            executable,
            f"{Path(__file__).parent.absolute()}/bgpy.py",
            f"{host}",
            f"{port}",
        ]
    )
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
):
    with ClientSocket() as cs:
        cs.connect(host, port)
        msg = Message(MessageType.EXEC, args=exec_args)
        res = cs.send(msg, await_response=await_response)
        return res.get_args()


def respond(client_socket: ClientSocket, response: dict):
    msg = Message(MessageType.OK, args=response)
    res = client_socket.send(msg)
    return res.get_args()


def terminate(
    exit_args: dict = {},
    await_response: bool = False,
    host: str = BG_HOST,
    port: int = BG_PORT,
):
    with ClientSocket() as cs:
        cs.connect(host, port)
        msg = Message(MessageType.EXIT, args=exit_args)
        res = cs.send(msg, await_response=await_response)
        return res.get_args()
