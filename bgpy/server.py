from message import Message, MessageType
from sockets import ClientSocket, ServerSocket

# Server
INIT = False
EXIT = False

with ServerSocket() as ss:

    while not EXIT:

        sock = ss.accept()

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
                    if msg.get_args()["await_response"]:
                        print("RESP!")
                        res = Message(
                            MessageType.OK,
                            args={
                                "message": "Response to request",
                                "reponse": {"param", "value"},
                            },
                        )
                        cs.send(res)
