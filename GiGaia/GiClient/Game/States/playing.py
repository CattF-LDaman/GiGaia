
from GiGaia.GiClient.Game.state import State
from GiGaia.GiClient.Game.Interfaces.playing import Playing as PlayingUI

from GiGaia.GiClient.Game.Entity.manager import EntityManager
from GiGaia.GiClient.Game.World.world import World
from GiGaia.GiClient.Game.scene import Scene

from GiGaia.GiCore.Game.states import STATE_IDS as SIDS

import pygame

class Playing(State):

    def __init__(self, game):

        super().__init__(game, SIDS.PLAYING, PlayingUI)

        self.scene = Scene(game)

        self.world = World(self)
        self.entity_manager = EntityManager(self)

        self.cam_speed = 500

        self.last_game_tick = 0
        self.ms_per_tick = int(1000/State.TICKRATE)

    @property
    def player(self):
        if self.player_eid and self.player_eid in self.entity_manager.entities:
            return self.entity_manager.entities[self.player_eid]

    def setup(self):

        self.player_eid = self.p.recv("SC_PLAYER").eid

    def handle_movement(self):

        p = pygame.key.get_pressed()

        if p[self.keybinds.MOVE_UP]:
            self.p.send("CS_MOVE", {"x":0, "y":-self.cam_speed})
        if p[self.keybinds.MOVE_DOWN]:
            self.p.send("CS_MOVE", {"x":0, "y":self.cam_speed})
        if p[self.keybinds.MOVE_LEFT]:
            self.p.send("CS_MOVE", {"x":-self.cam_speed, "y":0})
        if p[self.keybinds.MOVE_RIGHT]:
            self.p.send("CS_MOVE", {"x":self.cam_speed, "y":0})

    def tick(self):
        
        self.world.update()
        self.entity_manager.update()

        if self.game.client.ticks-self.last_game_tick > self.ms_per_tick:

            self.handle_movement()

            self.last_game_tick = self.game.client.ticks
