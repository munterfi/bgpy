Changelog
=========

This packages uses `semantic versions <https://semver.org/>`_.

Version 0.1.0
-------------

- Initial release of the **bgpy** on pypi.org package; Running local or remote python servers in the background and establish stream socket-based communication with clients. 
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
    - :code:`install.sh`: Builds the package and installs it to the global python version.
    - :code:`check.sh`: Automates checks and documentation build.
