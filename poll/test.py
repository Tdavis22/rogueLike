import socket

class IRCClient(object):
    def __init__(self, username, nickname=None, real_name=None):
        self.username = username
        self.nickname = nickname or username
        self.real_name = real_name or username
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def connect(self, address, port):
        self.socket.connect((address, port))
        self.send("NICK %s" % self.nickname)
        self.send("USER %s 0 * :%s" % (self.username, self.real_name))
    def send(self, data):
        self.socket.send((data + "\r\n").encode())
    def poll(self):
        buffer = ""
        while True:
            buffer += self.socket.recv(8192).decode()
            while "\r\n" in buffer:
                #line, _, buffer = buffer.partition("\r\n")
                line, buffer = buffer.split("\r\n", maxsplit=1)
                print(line)
                command, *params = line.split()
                if command == "PING":
                    self.send("PONG %s" % params[0])

client = IRCClient("fbwright_bot")
client.connect("chat.freenode.net", 6667)
client.poll()
