
from GiGaia.GiCore.logging import Logger
from GiGaia.GiCore.version import VERSION_STRING
from GiGaia.GiCore.Data import get_data_dir
from GiGaia.GiCore.Data.Assets import AssetsManager

from GiGaia.GiServer.Terminal.terminal import Terminal
from GiGaia.GiServer.Networking import connections
from GiGaia.GiServer.Data.directories import create_directory_structure
from GiGaia.GiServer.Data.config import Config
from GiGaia.GiServer.traffic import TrafficManager
from GiGaia.GiServer.Game.game import Game

import os
import sys
import time
import shutil
import pygame

pygame.init()

class Server:

    def __init__(self, server_directory=get_data_dir("GiGaiaServer"), dev=False):

        self.dev = dev

        self.server_directory = server_directory

        self.session_id = os.urandom(4)
        self.start_time = time.time()

        self.dirs = create_directory_structure(self.server_directory)

        self.config = Config(self.dirs["configs"])

        self.log_file_path = os.path.join(self.dirs["logs"], f"GiServer_{self.session_id.hex()}_{int(self.start_time)}.log")
        self.logger = Logger(self.log_file_path, self.config.logging)
        self.log = self.logger.log
        print(f"Logs for current session can be found at ' {self.log_file_path} ''")

        self.log(f"GiServer with version {VERSION_STRING} on {sys.platform}", 10)

        if self.dev:
            self.log("Running GiGaia in development mode!", 3)
            shutil.copytree("GiGaia_Assets",self.dirs["assets"], dirs_exist_ok=True)
            self.log("Assets duplicated to data directory.")

        self.assets = AssetsManager(self)
        self.assets.load()

        self.clients = []
        self.user_clients = {}

        self.terminal = Terminal(self)
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
        self.game.leave(client)
        client.close()
        self.log(f"Client {client.identifier} removed.")

    def close(self,exit_code=0):

        if exit_code == 0:
            self.log("Server closed.")
        else:
            self.log(f"Server closed with exit code {exit_code}")

        self.game.running = False
        self.terminal.running = False

        self.logger.close()

        sys.exit(exit_code)

    def run(self):

        self.log("Server starting...")

        connections.accept_connections(self)
        self.game.loop()

        self.terminal.run()
