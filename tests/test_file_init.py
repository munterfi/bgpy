#!/usr/bin/env python

"""Tests for `bgpy.client` and `bgpy.server` modules."""

from bgpy.core.environment import PORT, HOST
from bgpy.client import Client
from bgpy.server import Server
from bgpy.example.tasks import init_task, exec_task, exit_task
from bgpy.core.token import token_create
from pathlib import Path
import importlib.resources as resources

LOG_FILE = Path("tests/test_file_init.log")
LOG_LEVEL = "DEBUG"
PORT = PORT + 3
TOKEN = token_create()
with resources.path("bgpy.example", "tasks.py") as file_path:
    INIT_FILE = file_path

# Create server context
server = Server(
    host=HOST,
    port=PORT,
    token=TOKEN,
    log_level=LOG_LEVEL,
    log_file=LOG_FILE,
    init_file=INIT_FILE,
)

# Start server in background
server.run_background()

# Bind client to context
client = Client(
    host=HOST, port=PORT, token=TOKEN, log_level=LOG_LEVEL, log_file=LOG_FILE
)

# Send second INIT message from client to server, receive ERROR
res_init_error = client.initialize(init_task, exec_task, exit_task)


def test_file_initialize_error():
    assert res_init_error["message"] == "Already initialized."


# Execute command 'increase' with value on server, receive OK
res_exec_1 = client.execute({"command": "increase", "value_change": 10})


# Execute command 'decrease' with value on server, receive OK
res_exec_2 = client.execute({"command": "decrease", "value_change": 100})


def test_file_execution():
    assert res_exec_1["message"] == "Received 'EXEC'"
    assert res_exec_2["message"] == "Received 'EXEC'"


# Terminate and wait for response, receive OK with values
res_exit = client.terminate(await_response=True)


def test_file_terminate():
    assert isinstance(res_exit, dict)
    assert res_exit["request_count"] == 3
