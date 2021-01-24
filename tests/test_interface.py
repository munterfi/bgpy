#!/usr/bin/env python

"""Tests for `bgpy.interface` module."""

from bgpy.environment import HOME
from bgpy.example.tasks import init_task, exec_task, exit_task
from bgpy.interface import initialize, execute, terminate

LOG_FILE = HOME / "test_interface.log"

# Start background process
initialize(init_task, exec_task, exit_task, log_file=LOG_FILE)

# Increase value
execute({"command": "increase", "value_change": 10}, log_file=LOG_FILE)

# Decrease value
execute({"command": "decrease", "value_change": 100}, log_file=LOG_FILE)

# Terminate
args = terminate(await_response=True, log_file=LOG_FILE)


def test_request_count():
    assert isinstance(args, dict)
