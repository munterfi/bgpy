from .environment import (
    BACKLOG_SIZE,
    HEADER_SIZE,
    BUFFER_SIZE,
)
from .log import Log
from .message import Message, MessageType
from .serialize import serialize, deserialize
from contextlib import ContextDecorator
from pathlib import Path
from socket import (
    AF_INET,
    error,
    SHUT_WR,
    SO_REUSEADDR,
    SOCK_STREAM,
    socket,
    SOL_SOCKET,
)
from time import sleep
from typing import Optional


class ClientSocket(ContextDecorator):
    """
    Client socket

    Stream socket used on the client and the server to communciate.
    """

    __slots__ = ["sock", "log"]

    def __init__(
        self,
        sock: socket = None,
        log_level: str = "WARNING",
        log_file: Optional[Path] = None,
    ) -> None:
        """
        Initializes a object of type 'ClientSocket'.

        Parameters
        ----------
        sock : socket, optional
            An existing stream socket to use or None to create a new one,
            by default None.
        log_level : str, optional
            The level to log on (DEBUG, INFO, WARNING, ERROR or CRITICAL),
            by default WARNING.
        log_file : Optional[Path], optional
            Path to the file for writing the logs, by default None.
        """
        if sock is None:
            self.log = Log(__name__, log_level, "Client", log_file)
            self.sock = socket(AF_INET, SOCK_STREAM)
        else:
            self.log = Log(__name__, log_level, "Server", log_file)
            self.sock = sock
            host, port = self.sock.getpeername()
            self.log.info(f"ClientSocket connected to '{host}:{port}'")

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.sock.shutdown(SHUT_WR)
        self.sock.close()
        self.log.info("ClientSocket closed")
        return False

    def connect(self, host: str, port: int) -> None:
        """
        Connect to port on host.

        Parameters
        ----------
        host : str, optional
            Address or name of the host
        port : int, optional
            Port on the host to connect to

        Raises
        ------
        error
            If the socket connection fails, the error is also written to the
            logs and raised.
        """
        try:
            self.sock.connect((host, port))
            host, port = self.sock.getpeername()
            self.log.info(f"ClientSocket connected to '{host}:{port}'")
        except error as e:
            self.log.exception("ClientSocket failed to connected")
            raise error(e)

    def send(
        self, msg: Message, await_response: bool = False
    ) -> Optional[Message]:
        """
        Send a message to client socket.

        Send a message to a connected client socket via the network buffer. By
        default, after the message is sent and a confirmation message is
        received the method returns. If 'await_response' is set to True, after
        receiving the confirmation, the socket waits for another response by
        the remote client socket, which is again confirmed if received.

        Note
        ----
        If 'await_response' is set to True, but the remote client socket is not
        sending a response, this socket is waiting forever.

        Parameters
        ----------
        msg : Message
            Message to send to the remote client socket.
        await_response : bool, optional
            Waits for another response (after confirmation of the request) by
            the remote client socket, by default False

        Returns
        -------
        Message
            The confirmation message of the remote client socket. Or, if
            'await_response' is set to True, a custom response from the remote
            client socket.
        """
        self.log.info(f"Sending '{msg}'")
        args = msg.get_args()
        args["await_response"] = await_response
        msg.set_args(args)
        msg_enc = serialize(msg)
        self._buffered_send(msg_enc)
        res_enc = self._buffered_recv()
        if res_enc is None:
            return None
        res = deserialize(res_enc)
        self.log.info(f"Received '{res}'")
        if await_response:
            self.log.info("Waiting for response")
            res_2 = self.recv()
            if res_2 is None:
                return None
            else:
                return res_2
        return res

    def _buffered_send(self, msg: bytes) -> None:
        """
        Send message with header.

        Adds a header with the messages length to the message as prefix and
        sends the message to the network buffer of a connected client socket.

        Parameters
        ----------
        msg : bytes
            The message to send (all types) with arguments as bytes.

        Returns
        -------
            None
        """
        msg = bytes(f"{len(msg):<{HEADER_SIZE}}", "utf-8") + msg
        self.sock.sendall(msg)
        sleep(0.1)  # Give receiver time to complete reading.

    def recv(self) -> Optional[Message]:
        """
        Receive message from client socket.

        Receive a message from the connected client socket, by reading the
        network buffer.

        Returns
        -------
        Optional[Message]
            A message of type OK or Error.
        """
        msg_enc = self._buffered_recv()
        if msg_enc is None:
            return None
        msg = deserialize(msg_enc)
        res_msg = f"Received '{msg}'"
        self.log.info(res_msg)
        res = Message(MessageType.OK, args={"message": res_msg})
        self.log.info(f"Responding '{res}'")
        res_enc = serialize(res)
        self._buffered_send(res_enc)
        return msg

    def _buffered_recv(self) -> Optional[bytes]:
        """
        Receive message from network buffer.

        Reads chunks with length 'BUFFER_SIZE' from the network buffer.
        In the header with size 'HEADER_SIZE' of the first chunk, the total
        message length is stored. Chunks are received until the total message
        length is reached. Then, the function returns the message without the
        header of the first chunk. If the remote socket is closed (msg == b""),
        None is returned.

        Returns
        -------
            bytes or None: The concatenated message from the network buffer or
            None if the remote socket is closed.
        """
        msg = b""
        chunk_count = 0
        while True:
            chunk_count += 1
            chunk = self.sock.recv(BUFFER_SIZE)
            if chunk == b"":
                return None
            if chunk_count == 1:
                msg_len = int(chunk[:HEADER_SIZE])
                self.log.debug(f"Detected chunk header, length={msg_len}")
            msg += chunk
            if len(msg) - HEADER_SIZE == msg_len:
                self.log.debug(f"Message complete with chunks={chunk_count}")
                return msg[HEADER_SIZE:]


class ServerSocket(ContextDecorator):
    """
    Server socket

    Socket used on the server to listen on a port for requests.
    If the server accepts a connection request a new client socket for the
    communication is created, which binds to the client socket on the client.
    """

    __slots__ = ["sock", "log"]

    def __init__(
        self,
        host: str,
        port: int,
        backlog: int = BACKLOG_SIZE,
        log_level: str = "WARNING",
        log_file: Optional[Path] = None,
    ) -> None:
        """
        Initializes a object of type 'ServerSocket'.

        Parameters
        ----------
        host : str, optional
            Address or name of the host, by default BG_HOST
        port : int, optional
            Port on the host to listen to, by default BG_PORT
        backlog : int, optional
            Size of the backlog/queue of clients on the server,
            by default BG_BACKLOG
        log_level : str, optional
            The level to log on (DEBUG, INFO, WARNING, ERROR or CRITICAL),
            by default WARNING.
        log_file : Optional[Path], optional
            Path to the file for writing the logs, by default None.

        Raises
        ------
        error
            If the socket connection fails, the stack trace is also written to
            the logs and raised.
        """
        self.log = Log(__name__, log_level, "Server", log_file)
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        try:
            self.sock.bind((host, port))
            self.log.info(f"ServerSocket listening to '{host}:{port}'")
        except error as e:
            self.log.exception(
                f"ServerSocket failed to bind to '{host}:{port}'"
            )
            raise error(e)
        self.sock.listen(backlog)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.sock.close()
        self.log.info("ServerSocket closed")
        return False

    def accept(self) -> socket:
        """
        Accepts connection requests from client sockets and creates a client
        socket for the communication.

        Returns
        -------
        socket
            Returns a client socket on the server to communicate with the
            remote client socket.
        """
        client_socket, address = self.sock.accept()
        return client_socket
