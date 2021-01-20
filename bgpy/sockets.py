from .environment import (
    BG_HOST,
    BG_PORT,
    BG_LOG_FILE,
    BG_BACKLOG,
    BG_HEADER_SIZE,
    BG_BUFFER_SIZE,
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
from typing import Union


class ClientSocket(ContextDecorator):
    """
    Client socket

    Stream socket used on the client and the server to communciate.
    """

    def __init__(
        self,
        sock: socket = None,
        log_file: Path = BG_LOG_FILE,
        verbose: bool = True,
    ) -> None:
        """
        Initializes a object of type 'ClientSocket'.

        Parameters
        ----------
        sock : socket, optional
            An existing stream socket to use or None to create a new one,
            by default None
        log_file : Path, optional
            Path to write the logs, by default BG_LOG_FILE
        verbose : bool, optional
            Print logs also to the screen, by default True
        """
        if sock is None:
            self.log = Log(log_file, "Client", verbose)
            self.sock = socket(AF_INET, SOCK_STREAM)
        else:
            self.log = Log(log_file, "Server", verbose)
            self.sock = sock
            host, port = self.sock.getpeername()
            self.log.write(f"ClientSocket connected to '{host}:{port}'")

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.sock.shutdown(SHUT_WR)
        self.sock.close()
        self.log.write("ClientSocket closed")
        return False

    def connect(self, host: str = BG_HOST, port: int = BG_PORT):
        """
        Connect to port on host.

        Parameters
        ----------
        host : str, optional
            Address or name of the host, by default BG_HOST
        port : int, optional
            Port on the host to connect to, by default BG_PORT

        Raises
        ------
        error
            If the socket connection fails, the error is also written to the
            logs and raised.
        """
        try:
            self.sock.connect((host, port))
            host, port = self.sock.getpeername()
            self.log.write(f"ClientSocket connected to '{host}:{port}'")
        except error as e:
            self.log.write(str(e))
            raise error(e)

    def send(self, msg: Message, await_response: bool = False) -> Message:
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
        self.log.write(f"Sending '{msg}'")
        args = msg.get_args()
        args["await_response"] = await_response
        msg.set_args(args)
        msg = serialize(msg)
        self._buffered_send(msg)
        res = self._buffered_recv()
        if res is None:
            return None
        res = deserialize(res)
        self.log.write(f"Received '{res}'")
        if await_response:
            self.log.write("Waiting for response")
            res = self.recv()
            if res is None:
                return None
        return res

    def _buffered_send(self, msg: Message) -> None:
        """
        Send message with header.

        Adds a header with the messages length to the message as prefix and
        sends the message to the network buffer of a connected client socket.

        Parameters
        ----------
        msg : Message
            The message to send (all types) with arguments.

        Returns
        -------
            None
        """
        msg = bytes(f"{len(msg):<{BG_HEADER_SIZE}}", "utf-8") + msg
        self.sock.sendall(msg)
        sleep(0.1)  # Give receiver time to complete reading.

    def recv(self) -> Message:
        """
        Receive message from client socket.

        Receive a message from the connected client socket, by reading the
        network buffer.

        Returns
        -------
        Message
            A message of type OK or Error
        """
        msg = self._buffered_recv()
        if msg is None:
            return None
        msg = deserialize(msg)
        res_msg = f"Received '{msg}'"
        self.log.write(res_msg)
        res = Message(MessageType.OK, args={"message": res_msg})
        self.log.write(f"Responding '{res}'")
        res = serialize(res)
        self._buffered_send(res)
        return msg

    def _buffered_recv(self) -> Union[bytes, None]:
        """
        Receive message from network buffer.

        Reads chunks with length 'BG_BUFFER_SIZE' from the network buffer.
        In the header with size 'BG_HEADER_SIZE' of the first chunk, the total
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
            chunk = self.sock.recv(BG_BUFFER_SIZE)
            if chunk == b"":
                return None
            if chunk_count == 1:
                msg_len = int(chunk[:BG_HEADER_SIZE])
                # self.log.write(f"Detected chunk header, length={msg_len}")
            msg += chunk
            if len(msg) - BG_HEADER_SIZE == msg_len:
                # self.log.write(f"Message complete with chunks={chunk_count}")
                return msg[BG_HEADER_SIZE:]


class ServerSocket(ContextDecorator):
    """
    Server socket

    Socket used on the server to listen on a port for requests.
    If the server accepts a connection request a new client socket for the
    communication is created, which binds to the client socket on the client.
    """

    def __init__(
        self,
        host: str = BG_HOST,
        port: int = BG_PORT,
        backlog: int = BG_BACKLOG,
        log_file: Path = BG_LOG_FILE,
        verbose: bool = True,
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
        log_file : Path, optional
            Path to write the logs, by default BG_LOG_FILE
        verbose : bool, optional
            Print logs also to the screen, by default True

        Raises
        ------
        error
            If the socket connection fails, the error is also written to the
            logs and raised.
        """
        self.log = Log(log_file, "Server", verbose)
        self.log.clear()
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
        self.log.write("ServerSocket closed")
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
