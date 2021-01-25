from ..core.sockets import ClientSocket
from ..server import respond


def init_task() -> dict:
    init_args = {"request_count": 0, "value": 1000}
    return init_args


def exec_task(
    client_socket: ClientSocket, init_args: dict, exec_args: dict
) -> dict:
    init_args["request_count"] += 1
    if exec_args["command"] == "increase":
        init_args["value"] += exec_args["value_change"]
    if exec_args["command"] == "decrease":
        init_args["value"] -= exec_args["value_change"]
    return init_args


def exit_task(
    client_socket: ClientSocket, init_args: dict, exit_args: dict
) -> None:
    init_args["request_count"] += 1
    init_args["status"] = "Exited."
    respond(client_socket, init_args)
    return None
