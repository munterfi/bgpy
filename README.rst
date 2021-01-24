
====
bgpy
====

.. image:: https://img.shields.io/pypi/v/bgpy.svg
        :target: https://pypi.python.org/pypi/bgpy

.. image:: https://github.com/munterfinger/bgpy/workflows/check/badge.svg
        :target: https://github.com/munterfinger/bgpy/actions?query=workflow%3Acheck

.. image:: https://readthedocs.org/projects/bgpy/badge/?version=latest
        :target: https://bgpy.readthedocs.io/en/latest/
        :alt: Documentation Status

.. image:: https://codecov.io/gh/munterfinger/bgpy/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/munterfinger/bgpy


Running local or remote Python servers in the background using the subprocess
module and establish stream socket-based communication with clients in both
directions.

Features:

* Start and initialize a server process with a simple Python script. Once this parent script is terminated, the server process continues to run in the background.
* Send Python objects between the server and client processes (stored in a :code:`dict`) without worrying about serialization, message length, chunksize in the network buffer, and setting up server and client sockets.
* Due to the socket-based communication between server and client, it is possible to resume the communication from any location, as long as access to the same network is given and the hostname and port on which the server is listening is known.
* The communication between client and server is operating system independent (not like FIFO pipes for example). Furthermore, on Windows it is possible to communicate between the Windows Subsystem for Linux (WSL) and the Windows host system using bgpy.
* Optionally start the server on the remote using the command line interface (:code:`bgpy server <host> <port>`), and initialize it from the client (:code:`initialize(host, port, init_task, exec_task, exit_task)`) using Python.

Getting started
---------------

Get the stable release of the package from pypi:

.. code-block:: shell

    pip install bgpy


Run an example background process on localhost and communicate using stream sockets:

.. code-block:: python

    from bgpy.interface import initialize, execute, terminate
    from bgpy.example.tasks import init_task, exec_task, exit_task

    # Start background process
    initialize(init_task, exec_task, exit_task)

    # Increase value
    execute({"command": "increase", "value_change": 10})

    # Decrease value
    execute({"command": "decrease", "value_change": 100})

    # Terminate
    args = terminate(await_response=True)

License
-------

This project is licensed under the MIT License - see the LICENSE file for details