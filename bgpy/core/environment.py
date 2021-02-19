from pathlib import Path

# Paths
HOME = Path.home() / ".bgpy"
HOME.mkdir(parents=True, exist_ok=True)

# Sockets
HOST = "127.0.0.1"  # IP adress of the Server, default localhost
PORT = 54321  # Port used by server
STARTUP_TIME = 1  # Time to sleep before sending INIT message to a new server
BACKLOG_SIZE = 3  # Backlog size of the server socket (client queue)

# Network buffer
HEADER_SIZE = 16  # Size of the header of the first chunk (message length)
BUFFER_SIZE = 1024 * 2  # Size of the vjunks in the network buffer

# Logs
LOG_FILE = None
LOG_LEVEL = "INFO"
LOG_FORMAT = "[%(asctime)s - %(levelname)s] %(message)s (%(name)s)"
LOG_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
