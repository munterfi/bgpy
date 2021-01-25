#!/usr/bin/env python

"""Tests for `bgpy.cli` module."""

from bgpy.core.environment import HOME, HOST, PORT, STARTUP_TIME
from time import sleep
from subprocess import Popen

LOG_FILE = HOME / "test_cli.log"

# Start background process
start = Popen(
    ["bgpy", "server", f"{HOST}", f"{PORT}", f"--log-file={LOG_FILE}"]
)

# Wait to ensure client socket does not miss server socket
sleep(STARTUP_TIME)

# Terminate
stop = Popen(
    ["bgpy", "terminate", f"{HOST}", f"{PORT}", f"--log-file={LOG_FILE}"]
)

# Wait to ensure server socket is shut down, before next test starts
sleep(STARTUP_TIME)


def test_cli_success():
    assert isinstance(start, Popen)
    assert isinstance(stop, Popen)
