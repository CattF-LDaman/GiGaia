
from POA.POACore.Networking import DEFAULT_SERVER_PORT
from POA.POACore.logging import Logger
from POA.POACore.version import VERSION_STRING
from POA.POACore.Data.data import get_data_dir

from POA.POAServer.Terminal.terminal import Terminal
from POA.POAServer.Networking import connections
from POA.POAServer.Data.directories import create_directory_structure
from POA.POAServer.Data.config import Config
from POA.POAServer.traffic import TrafficManager
from POA.POAServer.Game.game import Game

import os
import sys
import time

class Server:

    def __init__(self,server_directory=get_data_dir("PlanOfActionServer")):

        self.server_directory = server_directory

        self.session_id = os.urandom(4)
        self.start_time = time.time()

        self.dirs = create_directory_structure(self.server_directory)

        self.config = Config(self.dirs["configs"])

        self.log_file_path = os.path.join(self.dirs["logs"], f"POAServer_{self.session_id.hex()}_{int(self.start_time)}.log")
        self.logger = Logger(self.log_file_path, self.config.logging)
        self.log = self.logger.log
        print(f"Logs for current session can be found at ' {self.log_file_path} ''")

        self.log(f"POAServer with version {VERSION_STRING} on {sys.platform}")

        self.clients = []
        self.user_clients = {}

        self.traffic = TrafficManager(self)
        self.game = Game(self)

        self.log("Server initialised.")

    def identify(self, cid):
        cid = cid.strip()
        if cid in self.user_clients:
            return self.user_clients[cid]
        else:
            for c in self.clients:
                if c.addr[0] == cid:
                    return c
                elif c.full_address == cid:
                    return c
                elif c.identifier == cid:
                    return c

    def join(self, client):
        self.clients.append(client)
        self.user_clients[client.username] = client
        self.traffic.register(client)
        self.game.join(client)
        client.start()

    def remove_client(self, client):

        self.clients.remove(client)
        self.user_clients.pop(client.username)
        client.close()
        self.log(f"Client {client.identifier} removed.")

    def close(self,exit_code=0):

        if exit_code == 0:
            self.log("Server closed.")
        else:
            self.log(f"Server closed with exit code {exit_code}")

        self.logger.close()

        sys.exit(exit_code)

    def start(self):

        self.log("Server starting...")

        connections.accept_connections(self)
        self.game.loop()

        Terminal(self).run()
