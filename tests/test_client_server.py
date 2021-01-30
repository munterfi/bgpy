#!/usr/bin/env python

"""Tests for `bgpy.client` and `bgpy.server` modules."""

from bgpy.core.environment import PORT, HOST, HOME, STARTUP_TIME
from bgpy.client import Client
from bgpy.server import Server
from bgpy.example.tasks import init_task, exec_task, exit_task
from time import sleep

LOG_FILE = HOME / "test_workflow.log"


# Create server context
server = Server(host=HOST, port=PORT, log_file=LOG_FILE)

# Start server in background
server.run_background()

# Bind client to context
client = Client(host=HOST, port=PORT, log_file=LOG_FILE)

# Send INIT message from client to server, receive OK
client.initialize(init_task, exec_task, exit_task)

# Send second INIT message from client to server, receive ERROR
client.initialize(init_task, exec_task, exit_task)

# Execute command 'increase' with value on server, receive OK
client.execute({"command": "increase", "value_change": 10})

# Execute command 'decrease' with value on server, receive OK
client.execute({"command": "decrease", "value_change": 100})

# Terminate and wait for response, receive OK with values
args = client.terminate(await_response=True)

sleep(STARTUP_TIME)


def test_request_count():
    assert isinstance(args, dict)
