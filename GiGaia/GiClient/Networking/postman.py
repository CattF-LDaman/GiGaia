from GiGaia.GiCore.threading import threaded_daemon
from GiGaia.GiCore.Networking.Packets import create_packet, read_packet, PACKET_NAMETYPES

import threading

class Postman:

    def __init__(self,game):

        self.game = game
        self.conn = game.conn

        self.active = False
        self.closed = False

        self.subscribers = {}
        self.outbox = {}

        self.holding = {}

        self.received = 0
        self.sent = 0
        self.dropped = 0

        self.can_send = threading.Event()

        self.waiting = {}
        self.__w_received = {}

        self.subscribe("A_PING", self.ping_recv)

    def start(self):

        self.active = True
        self.receiver()
        self.sender()

    def close(self, lost = False):

        if not self.closed:

            self.active = False
            self.conn.close()
            self.closed = True
            self.can_send.set()
            for w in self.waiting.values():
                w.set()
            self.game.client.log(f"Connection {'lost' if lost else 'closed'} with {self.conn.full_address}",3 if lost else 2)
            self.game.close("Connection lost." if lost else None)

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

    def ping_recv(self, ping_p):

        self.send("A_PING", {"timestamp":ping_p.timestamp})

    @threaded_daemon
    def receiver(self):

        try:
            while self.active:

                try:
                    in_bin = self.conn.recvsized()
                except Exception:
                    if self.conn.closed:
                        return
                    else:
                        raise

                if not in_bin:
                    self.close()

                try:
                    in_packet_type, in_packet = read_packet(in_bin)
                except Exception as e:
                    self.dropped += 1
                    self.game.client.log(f"Packet error: {type(e)}: {in_bin.hex()}", 4)

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

        except ConnectionError:
            self.close(True)

    @threaded_daemon
    def sender(self):

        try:
            while self.active:

                self.can_send.wait()

                if not self.active:
                    break

                for packet_type, packets in self.outbox.items():
                    for out_packet in packets:
                        self.conn.sendsized(create_packet(packet_type, out_packet or {}))
                        self.sent += 1
                    self.outbox[packet_type] = []

                self.can_send.clear()
        except ConnectionError:
            self.close(True)

    def _parse_packet_type(self, pt):

        if type(pt) == int:
            return pt
        elif type(pt) == str:
            return PACKET_NAMETYPES[pt]

    def send(self, packet_type, out_packet=None):
        packet_type = self._parse_packet_type(packet_type)

        if packet_type not in self.outbox:
            self.outbox[packet_type]= []
        self.outbox[packet_type].append(out_packet)
        self.can_send.set()

    def subscribe(self, packet_type, subscriber_inbox, unique=False):
        packet_type = self._parse_packet_type(packet_type)

        if packet_type not in self.subscribers or unique:
            self.subscribers[packet_type] = []

        self.subscribers[packet_type].append(subscriber_inbox)

    def unsubscribe(self, packet_type, subscriber_inbox):
        packet_type = self._parse_packet_type(packet_type)

        self.subscribers[packet_type].remove(subscriber_inbox)
        if len(self.subscribers[packet_type]) == 0:
            self.subscribers.pop(packet_type)

    def hold(self, packet_type):
        packet_type = self._parse_packet_type(packet_type)

        self.holding[packet_type] = []
        self.subscribe(packet_type, self.holding[packet_type], unique=True)

    def fetch(self, packet_type):
        packet_type = self._parse_packet_type(packet_type)

        if packet_type in self.holding and self.holding[packet_type]:
            out = self.holding[packet_type]
            self.hold(packet_type)

            return out
        
        return []
    
    def hold_all(self, *packet_types):

        for packet_type in packet_types:
            self.hold(packet_type)