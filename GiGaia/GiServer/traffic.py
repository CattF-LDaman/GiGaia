
class TrafficManager:

    def __init__(self,server):

        self.server = server

        self.outbox = []

        self.__packet_destinations = {} #{"entity":["P_ENT_UPD","P_ENT_DEST"]}
        self.inbox = {dest:[] for dest in self.__packet_destinations}

    def broadcast(self, packet_type, out_packet):

        for cun in self.server.user_clients:
            self.send(cun, packet_type, out_packet)

    def register(self, client):

        for destination, pts in self.__packet_destinations.items():
            for pt in pts:
                client.subscribe(pt, self.inbox[destination])

    def retrieve(self,inb):

        i = self.inbox[inb]
        self.inbox[inb] = []

        return i

    def send(self, user, packet_type, out_packet):
        self.outbox.append((user, packet_type, out_packet))

    def dispatch(self):

        for msg in self.outbox:

            if msg[0] not in self.server.user_clients:
                self.server.log(f"[TRAFFIC] Invalid destination for message: {msg[0]}", 1)
                continue

            self.server.user_clients[msg[0]].send(msg[1], msg[2])

        self.outbox.clear()
