# Background processes in python

## Main

Call the background processes using `Popen` from the `subprocess` module.

## Background

* background_plain.py: Nothing done on exit.
* background_gracful.py: Execute cleanup at the end of the iteration, delay.
* background_threading.py: Execute cleanup immediately when killed.

## License

MIT
