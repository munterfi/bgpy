from sockets import ClientSocket
from message import Message, MessageType
from time import sleep


# Client

with ClientSocket() as cs:
    cs.connect()
    msg = Message(MessageType.INIT, args={"test": "asdasd"})
    cs.send(msg)
    sleep(2)
    msg = Message(MessageType.EXEC, args={"test": "asdasd"})
    cs.send(msg)
    sleep(2)
    msg = Message(MessageType.EXIT, args={"test": "asdasd"})
    cs.send(msg)
