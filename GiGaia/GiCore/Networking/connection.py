
from GiGaia.GiCore.Networking.obf import SessionObfuscator

class Connection:

    def __init__(self,conn,addr,in_key,out_key):

        self.addr = addr
        self.conn = conn

        self.closed = False

        #self._obf = SessionObfuscator(in_key, out_key)

    @property
    def full_address(self):

        return f"{self.addr[0]}:{self.addr[1]}"

    def send(self,data):
        if self.closed:
            return None

        self.conn.send(data) #self.conn.send(self._obf.obf(data))

    def recv(self,n):
        if self.closed:
            return None

        in_bin = self.conn.recv(n)
        if not in_bin:
            raise ConnectionError("Connection closed.")
        return in_bin
        #return self._obf.deobf(in_bin)

    def sendsized(self,data,lensize=4):
        if self.closed:
            return None

        self.send(len(data).to_bytes(lensize,"little"))
        self.send(data)

    def recvsized(self,lensize=4):
        if self.closed:
            return None

        p_len = int.from_bytes(self.recv(lensize),"little")
        if p_len > 2**(lensize*8):
            raise ConnectionError("Packet size too large.")
        return self.recv(p_len)

    def close(self):

        self.closed = True
        self.conn.close()
