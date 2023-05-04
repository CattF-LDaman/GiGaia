
from GiGaia.GiCore.threading import threaded_daemon
from GiGaia.GiCore.Networking.Packets import read_packet, create_packet
from GiGaia.GiCore.Networking.Packets import PACKET_NAMETYPES

import threading
import time

class Handle:

    def __init__(self,server,conn,addr,username):

        self.server = server

        self.conn = conn
        self.addr = addr
        self.username = username

        self.active = False
        self.closed = False

        self.subscribers = {}
        self.outbox = {}

        self.received = 0
        self.sent = 0
        self.dropped = 0
        self.run_start = 0

        #self.can_send = threading.Event()
        self.can_send = threading.Semaphore()

        self.waiting = {}
        self.__w_received = {}

    @property
    def full_address(self):

        return f"{self.addr[0]}:{self.addr[1]}"

    @property
    def identifier(self):

        return f"{self.username}@{self.conn.full_address}"

    @property
    def seconds_active(self):
        return int(time.time()-self.run_start)

    @property
    def time_active(self):
        n = self.seconds_active
        day = n // (24 * 3600)
        n = n % (24 * 3600)
        hour = n // 3600
        n %= 3600
        minutes = n // 60
        n %= 60
        seconds = n
        return f"{day}D {hour}H {minutes}M {seconds}S"

    def start(self):

        self.run_start = time.time()
        self.active = True
        self.receiver()
        self.sender()

    def close(self, lost = False):

        if not self.closed:

            self.active = False
            self.closed = True
            if not lost:
                self.conn.close()
            self.can_send.release(10)
            for w in self.waiting.values():
                w.set()
            self.server.remove_client(self)
            self.server.log(f"Connection {'lost' if lost else 'closed'} with {self.identifier}",3 if lost else 2)

    def recv(self, packet_type, timeout=None):
        packet_type = self._parse_packet_type(packet_type)

        if packet_type not in self.waiting:
            self.waiting[packet_type] = threading.Event()

        self.__w_received[packet_type] = None

        self.waiting[packet_type].clear()
        c = self.waiting[packet_type].wait(timeout)
        if not c:
            self.__w_received.pop(packet_type)
            return None
        
        return self.__w_received.pop(packet_type)

    @threaded_daemon
    def receiver(self):

        try:
            while self.active:

                in_bin = self.conn.recvsized()
                if not in_bin:
                    self.close()
                in_packet_type, in_packet = read_packet(in_bin)

                self.received += 1

                if (in_packet_type not in self.subscribers or len(self.subscribers[in_packet_type]) == 0) and not in_packet_type in self.__w_received:

                    self.dropped += 1
                    continue

                if in_packet_type in self.__w_received:
                    self.__w_received[in_packet_type] = in_packet
                    self.waiting[in_packet_type].set()

                if in_packet_type in self.subscribers:

                    for inbox in self.subscribers[in_packet_type]:
                        if type(inbox) == list:
                            inbox.append(in_packet)
                        else:
                            inbox(in_packet)

        except ConnectionError as ce:
            self.close(True if "Connection closed" not in str(ce) and "[WinError 10054]" not in str(ce) else False)

    @threaded_daemon
    def sender(self):

        try:
            while self.active:

                self.can_send.acquire()

                if not self.active:
                    break

                for packet_type, packets in self.outbox.copy().items():
                    for out_packet in packets:
                        self.conn.sendsized(create_packet(packet_type, out_packet or {}))
                        self.sent += 1
                self.outbox.clear()

        except ConnectionError as ce:
            self.close(True if "Connection closed" not in str(ce) and "[WinError 10054]" not in str(ce) else False)

    def _parse_packet_type(self, pt):

        if type(pt) == int:
            return pt
        elif type(pt) == str:
            return PACKET_NAMETYPES[pt]

    def send(self,packet_type, out_packet=None):
        packet_type = self._parse_packet_type(packet_type)
        if packet_type not in self.outbox:
            self.outbox[packet_type]= []
        self.outbox[packet_type].append(out_packet)
        self.can_send.release()

    def subscribe(self, packet_type, subscriber_inbox):
        packet_type = self._parse_packet_type(packet_type)

        if packet_type not in self.subscribers:
            self.subscribers[packet_type] = []

        self.subscribers[packet_type].append(subscriber_inbox)

    def unsubscribe(self, packet_type, subscriber_inbox):
        packet_type = self._parse_packet_type(packet_type)

        self.subscribers[packet_type].remove(subscriber_inbox)
        if len(self.subscribers[packet_type]) == 0:
            self.subscribers.pop(packet_type)