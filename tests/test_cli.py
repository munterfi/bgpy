#!/usr/bin/env python

"""Tests for `bgpy.cli` module."""

from bgpy.environment import BG_HOST, BG_PORT, BG_SLEEP
from time import sleep
from subprocess import Popen

# Start background process
start = Popen(["bgpy", "server", f"{BG_HOST}", f"{BG_PORT}"])

# Wait to ensure client socket does not miss server socket
sleep(BG_SLEEP)

# Terminate
stop = Popen(["bgpy", "server", f"{BG_HOST}", f"{BG_PORT}"])


def test_cli_success():
    assert isinstance(start, Popen)
    assert isinstance(stop, Popen)
