from log import Log
from message import Message, MessageType
from environment import BG_HOST, BG_PORT, BG_LOG_FILE, BG_BACKLOG, BG_MSG_LEN
from serialize import serialize, deserialize
from pathlib import Path
from contextlib import ContextDecorator
from socket import socket, AF_INET, SOCK_STREAM, SHUT_WR, SOL_SOCKET, SO_REUSEADDR, error 


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
        self.sock.sendall(msg)
        res = self.sock.recv(BG_MSG_LEN)
        if len(msg) == 0:
            return None
        res = deserialize(res)
        self.log.write(f"Received '{res}'")
        return res

    def recv(self):
        msg = self.sock.recv(BG_MSG_LEN)
        if len(msg) == 0:
            return None
        msg = deserialize(msg)
        res_msg = f"Received '{msg}'"
        self.log.write(res_msg)
        res = Message(MessageType.OK, args={"message": res_msg})
        self.log.write(f"Responding '{res}'")
        res = serialize(res)
        self.sock.sendall(res)
        return msg


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
        #self.sock.shutdown(SHUT_RD)
        self.sock.close()
        self.log.write(f"ServerSocket closed")
        return False

    def accept(self):
        return self.sock.accept()
