from log import write_log
from threading import Event

exit = Event()


def main():
    write_log("Background process: Event started")
    i = 0
    while not exit.is_set():
        i = i + 1
        exit.wait(2)
        write_log(f"Background process: Event iteration {i}")  

    print("All done!")
    # Perform any cleanup here
    write_log("Background process: Event ended normally.")


def quit(signo, _frame):
    write_log(f"Background process: Event interrupted by {signo}, shutting down")
    # print("Interrupted by %d, shutting down" % signo)
    exit.set()


if __name__ == "__main__":

    import signal

    # No HUP signal on Windows, crashes yey ...
    # for sig in ('TERM', 'HUP', 'INT'): 
    for sig in ("TERM", "INT"):
        signal.signal(getattr(signal, "SIG" + sig), quit)

    main()
