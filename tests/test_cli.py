#!/usr/bin/env python

"""Tests for `bgpy.cli` module."""

from bgpy.core.environment import HOME, HOST, PORT
from subprocess import Popen, check_output

LOG_FILE = HOME / "test_cli.log"
PORT = PORT + 1

# Start background server
start = Popen(
    ["bgpy", "server", f"{HOST}", f"{PORT}", f"--log-file={LOG_FILE}"]
)


def test_cli_server():
    assert isinstance(start, Popen)


# Terminate
stop = Popen(
    ["bgpy", "terminate", f"{HOST}", f"{PORT}", f"--log-file={LOG_FILE}"]
)


def test_cli_terminate():
    assert isinstance(stop, Popen)


# Version
version = (
    check_output(["bgpy", "version"]).decode("utf-8").strip().split(" ")[1]
)


def test_cli_version():
    assert isinstance(version, str)
