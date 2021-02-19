# Sockets
HOST = "127.0.0.1"  # IP adress of the Server for testing
PORT = 54321  # Port used by server for testing
STARTUP_TIME = 1  # Time to sleep before sending INIT message to a new server
BACKLOG_SIZE = 3  # Backlog size of the server socket (client queue)

# Network buffer
HEADER_SIZE = 16  # Size of the header of the first chunk (message length)
BUFFER_SIZE = 1024 * 2  # Size of the vjunks in the network buffer

# Logs
LOG_LEVEL = "INFO"
LOG_FORMAT = ("[%(asctime)s %(process)d %(levelname)s] %(message)s (%(name)s)")
LOG_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
