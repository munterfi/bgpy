
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

Running local or remote python servers in the background using :code:`Popen` from the
subprocess module and establish stream socket-based communication with clients
in both directions.

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