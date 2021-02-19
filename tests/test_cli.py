#!/usr/bin/env python

"""Tests for `bgpy.cli` module."""

from bgpy.core.environment import HOME, HOST, PORT, STARTUP_TIME
from time import sleep
from subprocess import Popen, check_output

LOG_FILE = HOME / "test_cli.log"
LOG_LEVEL = "DEBUG"
PORT = PORT + 1

# Start background server
start = Popen(
    [
        "bgpy",
        "server",
        f"{HOST}",
        f"{PORT}",
        f"--log-level={LOG_LEVEL}",
        f"--log-file={LOG_FILE}",
    ]
)

# Wait for the server to startup
sleep(STARTUP_TIME)


def test_cli_server():
    assert isinstance(start, Popen)


# Terminate
stop = Popen(
    [
        "bgpy",
        "terminate",
        f"{HOST}",
        f"{PORT}",
        f"--log-level={LOG_LEVEL}",
        f"--log-file={LOG_FILE}",
    ]
)


def test_cli_terminate():
    assert isinstance(stop, Popen)


# Version
version = (
    check_output(["bgpy", "version"]).decode("utf-8").strip().split(" ")[1]
)


def test_cli_version():
    assert isinstance(version, str)
