
from GiGaia.GiCore.threading import threaded_daemon

from GiGaia.GiServer.Game.user import User

import pygame

class Game:

    def __init__(self,server):

        self.server = server
        self.config = server.config.game
        self.traffic = server.traffic

        self.running = True
        self.clock = pygame.time.Clock()

        self.users = {}

        self.dt = 0

    def join(self, client):

        self.users[client.username] = User(self, client)
        self.users[client.username].setup()

    @property
    def current_tickrate(self):
        return self.clock.get_fps()

    @threaded_daemon
    def loop(self):

        while self.running:

            self.dt = self.clock.tick(self.config.tickrate)

            for u in self.users.values():
                us = u.state
                if us.ready:
                    us.tick()

            self.traffic.dispatch()  # All outbound traffic should be ready for sending before this call
