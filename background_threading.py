from log import write_log, LOG_FILE
from threading import Event

exit = Event()

def main():
    i = 0
    while not exit.is_set():
      write_log(LOG_FILE, f"Background process: Threading iteration {i}")
      i = i + 1
      exit.wait(2)

    print("All done!")
    # perform any cleanup herie
    write_log(LOG_FILE, "Background process: Threading ended normally.")

def quit(signo, _frame):
    write_log(LOG_FILE, f"Background process: Threading interrupted by {signo}, shutting down")
    print("Interrupted by %d, shutting down" % signo)
    exit.set()

if __name__ == '__main__':

    import signal
    #for sig in ('TERM', 'HUP', 'INT'):
    for sig in ('TERM', 'INT'):
        #signal.signal(getattr(signal, 'SIG'+sig), quit);
        signal.signal(getattr(signal, 'SIG'+sig), quit);

    main()
