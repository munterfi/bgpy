from pathlib import Path

# Paths
BG_HOME = Path.home() / ".bgpy"
BG_HOME.mkdir(parents=True, exist_ok=True)
BG_LOG_FILE = BG_HOME / "bgpy.log"

# Sockets
BG_HOST = "127.0.0.1"  # IP adress of the Server, default localhost
BG_PORT = 50014  # Port used by server
BG_BACKLOG = 1  # Backlog size of the server socket (client queue)

# Network buffer
BG_HEADER_SIZE = 16  # Size of the header of the first chunk (message length)
BG_BUFFER_SIZE = 1024 * 2  # Size of the vjunks in the network buffer
