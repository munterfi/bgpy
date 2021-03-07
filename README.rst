
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

* Start and initialize a server process with a simple Python script. Once this
  parent script is terminated, the server process continues to run in the
  background.
* Send Python objects between the server and client processes (stored in a
  :code:`dict`) without worrying about authentication, Python object 
  serialization, setting up server and client sockets, message length, and
  chunksize in the network buffer.
* Due to the socket-based communication between server and client, it is
  possible to resume the communication from any location, as long as access to
  the same network is given and the hostname and port on which the server is
  listening is known.
* The communication between client and server is operating system independent
  (not like FIFO pipes for example). Furthermore, on Windows it is possible to
  communicate between the Windows Subsystem for Linux (WSL) and the Windows
  host system using bgpy.
* Optionally start the server on the remote using the command line interface
  (:code:`bgpy server <host> <port>`), and initialize it from the local client
  (:code:`initialize(host, port, init_task, exec_task, exit_task)`) using
  Python.

Getting started
---------------

Install the stable release of the package from pypi:

.. code-block:: shell

    pip install bgpy

Define tasks
^^^^^^^^^^^^

Run and intialize a bgpy server on a host, which starts listening
to the provided port. After starting the server, a INIT message with the
:code:`init_task`, :code:`exec_task()` and :code:`exit_task()` tasks are send
to the server in order to complete the initialization.

* **Initialization task**

Task that runs once during initialization and can be used to set up the
server. The return value of this function must be a dict, which is then
passed to the :code:`exec_task` function with every request by a client.

.. code-block:: python
    
    def init_task(client_socket: ClientSocket) -> dict:
        init_args = {"request_count": 0, "value": 1000}
        return init_args

* **Execution task**

Task that is called each time a request is made by a client to the server.
In this task the message from the :code:`execute` method of the :code:`Client`
class is interpreted and an action has to be defined accordingly. The
input of the :code:`exec_task` is the return value of the last
:code:`exec_task` function call (or if never called, the return value from the
:code:`init_task`). Using the function :code:`respond` om the server, a second
response can be sent to the client after the standard confirmation of the
receipt of the message by the server.

.. code-block:: python
    
    def exec_task(
        client_socket: ClientSocket, init_args: dict, exec_args: dict
    ) -> dict:
        init_args["request_count"] += 1
        if exec_args["command"] == "increase":
                init_args["value"] += exec_args["value_change"]
        if exec_args["command"] == "decrease":
                init_args["value"] -= exec_args["value_change"]
        return init_args

* **Exit task**

Task that is executed once if an exit message is sent to the server by
the :code:`terminate` method of the :code:`Client` class. The input of the
:code:`exit_task` is the return value of the last :code:`exec_task` function
call (or if never called, the return value from the :code:`init_task`). With
:code:`respond` a second message can be sent to the client, if the client is
set to be waiting for a second response
(:code:`Client.terminate(..., await_response=True`).

.. code-block:: python
    
    def exit_task(
        client_socket: ClientSocket, init_args: dict, exit_args: dict
    ) -> None:
        init_args["request_count"] += 1
        init_args["status"] = "Exited."
        respond(client_socket, init_args)
        return None

**Note:** If the client is set to wait for a second response
(:code:`Client.execute(..., await_response=True` or
:code:`Client.terminate(..., await_response=True`) it is important to handle
this on the server side by sending a response to the client using
:code:`respond`. Otherwise the client may be waiting forever as there is no
timeout specified.


Run the server
^^^^^^^^^^^^^^

Run an example background process on localhost and send requests using client
sockets:

.. code-block:: python

    from bgpy import Client, Server
    from bgpy.example.tasks import init_task, exec_task, exit_task

    HOST = "127.0.0.1"
    PORT = 54321

    # Optionally set a token for the client authentication
    from bgpy import token_create
    TOKEN = token_create()

    # Create server context
    server = Server(host=HOST, port=PORT, token=TOKEN)

    # Start server in background from context
    server.run_background()

    # Bind client to server context
    client = Client(host=HOST, port=PORT, token=TOKEN)

    # Send INIT message from client to server, receive OK
    response = client.initialize(init_task, exec_task, exit_task)

    # Execute command 'increase' with value on server, receive OK
    response = client.execute({"command": "increase", "value_change": 10})

    # Execute command 'decrease' with value on server, receive OK
    response = client.execute({"command": "decrease", "value_change": 100})

    # Terminate and wait for response, receive OK with values
    response = client.terminate(await_response=True)

License
-------

This project is licensed under the MIT License - see the LICENSE file for
details.
