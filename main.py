import socket 
from threading import Thread

class Server2Me(Thread):
    def __init__(self, host, port):
        super(Server2Me, self).__init__()
        self.client = None
        self.host = host
        self.port = port
        self.socket = socket.socket()
        self.socket.connect((host, port))

    def run(self):
        while True:
            self.data = self.socket.recv(1024)
            if self.data:
                print(f"[{self.host}:{self.port}] <- {self.data}")
                self.client.sendall(self.data)




class Me2Server(Thread):
    def __init__(self, host, port):
        super(Me2Server, self).__init__()
        self.server = None
        self.host = host
        self.port = port
        self.sock = socket.socket()
        self.sock.bind((host, port))
        self.sock.listen(1)
        self.conn, self.addr = self.sock.accept()

    def run(self):
        while True:
            self.data = self.conn.recv(1024)
            if self.data:
                print(f"[{self.host}:{self.port}] -> {self.data}")
                self.server.sendall(self.data)
            


class Proxy(Thread):
    def __init__(self, fhost, thost, fport, tport):
        super(Proxy, self).__init__()
        self.fhost = fhost
        self.thost = thost
        self.fport = fport
        self.tport = tport

    def run(self):
        print("[proxy] setting up")
        self.m2s = Me2Server(self.fhost, self.fport)
        self.s2m = Server2Me(self.thost, self.tport)
        print(f"[proxy] connection established")
        self.m2s.server = self.s2m.socket
        self.s2m.client = self.m2s.conn

        self.m2s.start()
        self.s2m.start()


proxy = Proxy("0.0.0.0", "89.223.126.198", 4444, 5555)
proxy.start()

