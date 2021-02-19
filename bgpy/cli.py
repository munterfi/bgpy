from .core.environment import LOG_LEVEL, LOG_FILE
from .server import Server
from .client import Client
from typer import Typer, echo, Abort
from typing import Optional
from pathlib import Path

try:
    from importlib import metadata
except ImportError:
    # Running on pre-3.8 Python; use importlib-metadata package
    import importlib_metadata as metadata  # type: ignore

app = Typer(add_completion=False)


@app.command("server")
def run_server(
    host: str,
    port: int,
    log_level: str = LOG_LEVEL,
    log_file: Optional[Path] = LOG_FILE,
) -> None:
    """Run a bgpy server on the given host, which starts listening to the
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
    host: str,
    port: int,
    log_level: str = LOG_LEVEL,
    log_file: Optional[Path] = LOG_FILE,
) -> None:
    """Terminate a bgpy server on the given host, which is listening to the
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
    """Version information of the package."""
    package = "bgpy"
    version = metadata.version(package)
    echo(f"{package} {version}")


def main():
    app()
