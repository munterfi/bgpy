============
Installation
============

Stable release
--------------

Get the stable release of **bgpy** from pypi:

.. code-block:: shell

    python3 -m pip install bgpy

From sources
------------

Or install the development version from `Github <https://github.com/munterfi/bgpy>`_:

.. code-block:: shell

    git clone git://github.com/munterfi/bgpy.git
    cd bgpy
    poetry install && poetry build
    cd dist && python3 -m pip install *.whl
