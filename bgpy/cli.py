from .server import Server
from .client import Client
from typer import Typer, echo, Abort, Argument, Option
from typing import Optional
from pathlib import Path

try:
    from importlib.metadata import version as get_version
except ImportError:
    from importlib_metadata import version as get_version  # type: ignore

app = Typer(add_completion=False)


@app.command("server")
def run_server(
    host: str = Argument(..., help="Host address to run the server on"),
    port: int = Argument(..., help="Port where the server should listen to"),
    log_level: str = Option(
        "INFO",
        "--log-level",
        "-l",
        help="Minimum level of the logs (DEBUG, INFO, WARNING, ERROR, ...)",
    ),
    log_file: Optional[Path] = Option(
        None, "--log-file", "-f", help="Path to a log file"
    ),
) -> None:
    """
    Start a bgpy server.

    Run a bgpy server on the given host, which starts listening to the
    provided port.
    Note: Before calling the 'initialize()' method of the 'Client' class and
    passing 'init_task()', exec_task()' and 'exit_task()' to the server, the
    server will not respond to requests.
    """
    if str(log_file) == "None":
        log_file = None
    server = Server(
        host=host, port=int(port), log_level=log_level, log_file=log_file
    )
    try:
        server.run()
    except OSError as e:
        echo(e)
        Abort()


@app.command("terminate")
def terminate_server(
    host: str = Argument(..., help="Host address of the server"),
    port: int = Argument(..., help="Port where the server is listening"),
    log_level: str = Option(
        "INFO",
        "--log-level",
        "-l",
        help="Minimum level of the logs (DEBUG, INFO, WARNING, ERROR, ...)",
    ),
    log_file: Optional[Path] = Option(
        None, "--log-file", "-f", help="Path to a log file"
    ),
) -> None:
    """
    Terminate a bgpy server.

    Terminate a bgpy server on the given host, which is listening to the
    provided port.
    """
    if str(log_file) == "None":
        log_file = None
    client = Client(
        host=host, port=int(port), log_level=log_level, log_file=log_file
    )
    try:
        client.terminate()
    except OSError as e:
        echo(e)
        Abort()


@app.command("version")
def version_info():
    """
    Version information.

    Prints the version information of the package.
    """
    package = "bgpy"
    version = get_version(package)
    echo(f"{package} {version}")


def main():
    app()
