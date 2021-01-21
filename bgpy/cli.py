from .server import run
from .interface import terminate
from typer import Typer, echo, Abort

try:
    from importlib import metadata
except ImportError:
    # Running on pre-3.8 Python; use importlib-metadata package
    import importlib_metadata as metadata  # type: ignore

app = Typer(add_completion=False)


@app.command("server")
def run_server(host: str, port: int) -> None:
    """Run a bgpy server

    Run a bgpy server on the given host, which starts listening to the provided
    port.
    Note: Before calling 'initialize()' and passing 'init_task()', exec_task()'
    and 'exit_task()' to the server, it will not respond to requests.
    """
    try:
        run(host=host, port=int(port))
    except OSError as e:
        echo(e)
        Abort()


@app.command("terminate")
def terminate_server(host: str, port: int) -> None:
    """Terminate a bgpy server

    Terminate a bgpy server on the given host, which is listening to the
    provided port.
    """
    try:
        terminate(host=host, port=int(port))
    except OSError as e:
        echo(e)
        Abort()


@app.command("version")
def version_info():
    """Version information

    Prints the version of the package.
    """
    package = "bgpy"
    version = metadata.version(package)
    echo(f"{package} {version}")


def main():
    app()
