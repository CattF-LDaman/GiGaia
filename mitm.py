from GiGaia.GiCore.threading import threaded_daemon
from GiGaia.GiCore.Networking.obf import SessionObfuscator
import socket
import sys
import string

PORT = 1234
TARGET = ("localhost", 17746)
CHUNK_SIZE = 4096

def accept_connections():

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    try:
        soc.bind(("", PORT))
    except OSError:
        print("COULDN'T BIND TO GIVEN PORT!")
        sys.exit(1)

    soc.listen()

    print("Started listening on socket.")
    print("Connections will now be accepted.")

    while True:
        conn, addr = soc.accept()

        print(f"New connection with {addr[0]}:{addr[1]}")

        ClientThread(conn,addr).start()

class ClientThread:

    PRINTABLE = bytes(string.printable, "ascii")

    def __init__(self, conn, addr):

        self.client_conn = conn
        self.client_conn.setblocking(0)
        self.addr = addr

        self.ext_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ext_conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        self.sent = 0
        self.recv = 0

        self.SRV_OBF = None
        self.CLN_OBF = None

    @threaded_daemon
    def start(self):

        self.ext_conn.connect(TARGET)
        self.ext_conn.setblocking(0)
        print(f"Starting {self.addr[0]}.")
        self.client_to_ext()
        self.ext_to_client()

    @threaded_daemon
    def client_to_ext(self):

        while True:
            try:
                self.ext_conn.send(pck := self.client_conn.recv(CHUNK_SIZE))
                self.sent += 1
                if self.SRV_OBF:
                    pck = self.SRV_OBF.deobf(pck)

                print(f"SENT #{self.sent} {self.addr[0]}: {len(pck)} bytes.\n{self.hexdump(pck)}")
                if self.sent == 2:
                    self.SRV_OBF = SessionObfuscator(pck[:256], None)

            except BlockingIOError:
                pass

    def ext_to_client(self):
        
        while True:
            try:
                self.client_conn.send(pck := self.ext_conn.recv(CHUNK_SIZE))
                self.recv += 1
                if self.CLN_OBF:
                    pck = self.CLN_OBF.deobf(pck)
                
                print(f"RECV #{self.recv}: {self.addr[0]}: {len(pck)} bytes.\n{self.hexdump(pck)}")
                
                if self.recv == 1:
                    self.CLN_OBF = SessionObfuscator(pck[:256], None)

            except BlockingIOError:
                pass


    '''
    Simple implementation of hexdump
    https://gist.github.com/JonathonReinhart/509f9a8094177d050daa84efcd4486cb
    '''
    def hexdump(self, data, length=16):
        filter = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
        lines = []
        digits = 4 if isinstance(data, str) else 2
        for c in range(0, len(data), length):
            chars = data[c:c+length]
            hex = ' '.join(["%0*x" % (digits, (x)) for x in chars])
            printable = ''.join(["%s" % (((x) <= 127 and filter[(x)]) or '.') for x in chars])
            lines.append("%04x  %-*s  %s\n" % (c, length*3, hex, printable))
        return ''.join(lines)

if __name__ == "__main__":
    accept_connections()