# Background processes in python

Running python background processes using Popen from the subprocess module and exit gracefully on Unix-like operating systems.

Execute `./run.sh`, which will start the main process and monitor log and processes.
Then you can kill the background processes manually and observe behaviour.

**Note:** Ending `run.sh` by hitting `ctrl+c` will only end the `background_gracful.py` and `background_event.py` processes while `background_plain.py` is still running.

## Main process

Calls the background processes using `Popen` from the `subprocess` module.

## Background process

Process writes to log and handles exit differently:

* `background_plain.py`: Nothing done on exit.
* `background_gracful.py`: Execute cleanup at the end of the iteration, delay.
* `background_event.py`: Execute cleanup immediately when killed.

## License

MIT

# References

* [GracefulKiller class](https://stackoverflow.com/questions/18499497/how-to-process-sigterm-signal-gracefully)
* [Event](https://stackoverflow.com/questions/5114292/break-interrupt-a-time-sleep-in-python/46346184#46346184)
