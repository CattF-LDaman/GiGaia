
from GiGaia.GiCore.threading import threaded_daemon

from GiGaia.GiServer.Game.user import User
from GiGaia.GiServer.Game.World import World
from GiGaia.GiServer.Game.Entity import EntityManager
from GiGaia.GiServer.Game.chat import Chat

import pygame

class Game:

    def __init__(self,server):

        self.server = server
        self.assets = server.assets
        self.log = server.log
        self.config = server.config.game
        self.traffic = server.traffic
        self.dirs = server.dirs

        self.running = True
        self.clock = pygame.time.Clock()

        self.users = {}
        self.players = {}

        self.dt = 0
        self.ticks = 0

        self.world = World(self)
        self.entity_manager = EntityManager(self)
        self.chat = Chat(self)

    def join(self, client):

        self.users[client.username] = User(self, client)
        self.users[client.username].setup()
        self.log(f"{client.username} joined the game.",3)
        self.chat.broadcast_chat("SYS",f"{client.username} joined the game.")

    def leave(self, client):

        self.users.pop(client.username).left = True
        if client.username in self.players:
            self.players.pop(client.username).leave()
        self.log(f"{client.username} left the game.",3)
        self.chat.broadcast_chat("SYS",f"{client.username} left the game.")

    @property
    def current_tickrate(self):
        return self.clock.get_fps()

    @threaded_daemon
    def loop(self):

        while self.running:

            self.dt = 1/self.config.tickrate
            self.clock.tick(self.config.tickrate*self.config.time_scale)
            self.ticks += self.clock.get_time()*self.config.time_scale

            for u in self.users.copy().values():
                if u.state.ready:
                    u.state.tick()

            self.world.tick()

            self.entity_manager.update()

            self.traffic.dispatch()  # All outbound traffic should be ready for sending before this call
