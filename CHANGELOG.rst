Changelog
=========

This package uses `semantic versions <https://semver.org/>`_.

Version 0.2.0.9000
------------------

- Features:
    - A token for authentication in the requests from the client to the server can now be set.
    - Added token module for handling tokens.
- Bugfixes:
  
Version 0.2.0
-------------

- Features:
    - CLI command :code:`bgpy version` to check for the version of the package.
    - Restructure environment variables, remove :code:`HOST` and :code:`PORT` from core socket classes.
    - Move log file handling to the interface, create seperate log file for each test and upload as artifacts in github action package check.
    - Split :code:`interface.py` into a :code:`Server` context class and a :code:`Client` context class.
    - Added :code:`__repr__` methods to :code:`Client`, :code:`Server` and :code:`Message` classes.
    - Define :code:`__slots__` for all classes.
    - Use :code:`logging` package from the standard library to perform logging tasks. Split logs at level INFO into STDOUT and STDERR on the stream handler for the console.
    - Documented CLI help pages.
    - Detailed usage section in README.
- Bugfixes:
    - Updated docstrings.
    - Cleaned environment and removed the need for a directory in the users home (:code:`~/.bgpy`).
    - Render module index and docstrings on readthedocs.
    - Pass mypy type checks.
    - Run sphinx-apidoc in :code:`check.sh` script to avoid errors in documentation build when changing submodule structure.

Version 0.1.0
-------------

- Initial release of the **bgpy** on pypi.org package; Running local or remote Python servers in the background and establish stream socket-based communication with clients. 
- Development setup:
    - :code:`poetry`: Managing dependencies and package build env.
    - :code:`pytest`: Framework for testing.
    - :code:`mypy`: Static type checking.
    - :code:`flake8`: Code linting.
    - :code:`sphinx`: Documentation of the package using :code:`numpydoc` docstring style.
- Submodules:
    - example: Example :code:`init_task`, :code:`exec_task` and :code:`exit_task` for testing.
    - cli: :code:`bgpy server <host> <port>` to run a server and :code:`bgpy terminate <host> <port>` to send exit message to a server.
- Scripts:
    - :code:`install.sh`: Builds the package and installs it to the global Python version.
    - :code:`check.sh`: Automates checks and documentation build.
