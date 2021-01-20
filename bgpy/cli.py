from .server import run
from .interface import terminate
from typer import Typer, echo, Abort

app = Typer(add_completion=False)


@app.command("server")
def run_server(host: str, port: int):
    """Run a bgpy server

    Run a bgpy server on the given host, which starts listening to the provided
    port.
    Note: Before calling 'initialize()' and passing 'init_task()', exec_task()'
    and 'exit_task()' to the server, it will not respond to requests.
    """
    echo(f"Starting bgpy server on {host}:{port} ...")
    try:
        run(host=host, port=int(port))
    except OSError as e:
        echo(e)
        Abort()


@app.command("terminate")
def terminate_server(host: str, port: int):
    """Terminate a bgpy server

    Terminate a bgpy server on the given host, which is listening to the
    provided port.
    """
    echo(f"Stopping bgpy server on {host}:{port} ...")
    try:
        terminate(host=host, port=int(port))
    except OSError as e:
        echo(e)
        Abort()


def main():
    app()
