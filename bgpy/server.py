from sockets import ClientSocket, ServerSocket
from message import Message, MessageType

# Server
INIT = False
EXIT = False

with ServerSocket() as ss:

    while not EXIT:

        sock, addr = ss.accept()

        with ClientSocket(sock=sock) as cs:
            while True:
                msg = cs.recv()
                if msg is None:
                    break

                if msg.type is MessageType.EXIT:
                    print("EXIT!")
                    EXIT = True
                    break

                if msg.type is MessageType.INIT:
                    print("INIT!")
                    INIT = True
                    continue

                if not INIT:
                    print("Initialize first!")
                    continue

                if msg.type is MessageType.EXEC:
                    print("EXEC!")

