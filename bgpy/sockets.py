from log import Log
from message import Message, MessageType
from environment import BG_HOST, BG_PORT, BG_LOG_FILE, BG_BACKLOG, BG_MSG_LEN
from serialize import serialize, deserialize
from pathlib import Path
from contextlib import ContextDecorator
from socket import (
    socket,
    AF_INET,
    SOCK_STREAM,
    SHUT_WR,
    SOL_SOCKET,
    SO_REUSEADDR,
    error,
)

HEADER_SIZE = 10
BUFFER_SIZE = 16


class ClientSocket(ContextDecorator):
    def __init__(
        self, sock=None, log_file: Path = BG_LOG_FILE, verbose: bool = True
    ) -> None:
        if sock is None:
            self.log = Log(log_file, "Client", verbose)
            self.sock = socket(AF_INET, SOCK_STREAM)
        else:
            self.log = Log(log_file, "Server", verbose)
            self.sock = sock
            host, port = self.sock.getsockname()
            self.log.write(f"ClientSocket connected to '{host}:{port}'")

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.sock.shutdown(SHUT_WR)
        self.sock.close()
        self.log.write(f"ClientSocket closed")
        return False

    def connect(self, host: str = BG_HOST, port: int = BG_PORT):
        try:
            self.sock.connect((host, port))
            self.log.write(f"ClientSocket connected to '{host}:{port}'")
        except error as e:
            self.log.write(e)
            raise error(e)

    def send(self, msg: Message):
        self.log.write(f"Sending '{msg}'")
        msg = serialize(msg)
        self._send(msg)
        res = self._recv()
        if len(msg) == 0:
            return None
        res = deserialize(res)
        self.log.write(f"Received '{res}'")
        return res

    def _send(self, msg):
        msg = bytes(f"{len(msg):<{HEADER_SIZE}}", "utf-8") + msg
        self.sock.sendall(msg)
        # time.sleep(0.1)  # Give receiver time to complete reading.

    def recv(self):
        msg = self._recv()
        if msg is None:
            return None
        if len(msg) == 0:
            return None
        msg = deserialize(msg)
        res_msg = f"Received '{msg}'"
        self.log.write(res_msg)
        res = Message(MessageType.OK, args={"message": res_msg})
        self.log.write(f"Responding '{res}'")
        res = serialize(res)
        self._send(res)
        return msg

    def _recv(self):
        # Setup empty message and count
        msg = b""
        chunk_count = 0

        while True:
            chunk_count += 1
            chunk = self.sock.recv(BUFFER_SIZE)

            if chunk == b"":
                return None

            # Get message length from header
            # Set new message to False, after header is read.
            if chunk_count == 1:
                msg_len = int(chunk[:HEADER_SIZE])
                print(f"Received chunk {chunk_count} with header: {msg_len}")
            else:
                print(f"Received chunk {chunk_count}")

            # Add chunk to message
            msg += chunk

            # Check if message is complete
            if len(msg) - HEADER_SIZE == msg_len:
                print(f"Message complete: {msg_len}")
                # Remove header
                return msg[HEADER_SIZE:]


class ServerSocket(ContextDecorator):
    def __init__(
        self,
        host: str = BG_HOST,
        port: int = BG_PORT,
        backlog: int = BG_BACKLOG,
        log_file: Path = BG_LOG_FILE,
        verbose: bool = True,
    ) -> None:
        self.log = Log(log_file, "Server", verbose)
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        try:
            self.sock.bind((host, port))
            self.log.write(f"ServerSocket listening to '{host}:{port}'")
        except error as e:
            self.log.write(e)
            raise error(e)
        self.sock.listen(backlog)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        # self.sock.shutdown(SHUT_RD)
        self.sock.close()
        self.log.write(f"ServerSocket closed")
        return False

    def accept(self):
        return self.sock.accept()
