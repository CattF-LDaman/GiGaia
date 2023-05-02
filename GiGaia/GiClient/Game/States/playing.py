
from GiGaia.GiClient.Game.state import State
from GiGaia.GiClient.Game.Interfaces.playing import Playing as PlayingUI

from GiGaia.GiClient.Game.Interfaces.PlayingUI.inventory import Inventory

from GiGaia.GiClient.Game.Entity.manager import EntityManager
from GiGaia.GiClient.Game.World.world import World
from GiGaia.GiClient.Game.scene import Scene
from GiGaia.GiClient.Game.States.Playing.inventory import PlayerInventory

from GiGaia.GiCore.Game.states import STATE_IDS as SIDS
from GiGaia.GiCore.Game.World.coords import pix_to_tileref, sum_coords, mult_coord

import pygame
import math

class Playing(State):

    def __init__(self, game):

        super().__init__(game, SIDS.PLAYING, PlayingUI)

        self.cam_speed = 500
        self.view_bob = 10
        self.view_bob_smooth = 80

        self.moving = False

        self.last_game_tick = 0
        self.ms_per_tick = int(1000/State.TICKRATE)

        self.player_eid = None

        self.p.subscribe("SC_PLAYER", self.set_player)

    @property
    def player(self):
        if self.player_eid and self.player_eid in self.entity_manager.entities:
            return self.entity_manager.entities[self.player_eid]

    def set_player(self, pp):

        self.player_eid = pp.eid

    def setup(self):

        self.scene = Scene(self.game)
        self.world = World(self)
        self.entity_manager = EntityManager(self)
        self.inventory = self.inv = PlayerInventory(self)

    def handle_event(self, event):

        match event.type:
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_F10:
                        for c in self.world.chunks.values():
                            c.updated = True
                    case self.keybinds.INVENTORY:
                        self.ui.open_window(Inventory)

    def handle_movement(self):

        p = pygame.key.get_pressed()
        self.moving = False

        if p[self.keybinds.JUMP]:
            self.player.jump()

        if p[self.keybinds.MOVE_LEFT]:
            self.player.move(-1)
            self.moving = True
        if p[self.keybinds.MOVE_RIGHT]:
            self.player.move(1)
            self.moving = True

        if p[self.keybinds.MOVE_DOWN] and p[self.keybinds.CROUCH]:
            self.player.crouch()

    def handle_wset(self):  # Temporary

        l = 1 if pygame.key.get_pressed()[pygame.K_LSHIFT] else 0
        chunk, tileref = pix_to_tileref(self.scene.mouse)

        mp = pygame.mouse.get_pressed()
        if mp[0]:
            self.p.send("CS_WSET", {"chunk":chunk, "tileref":tileref+(l,), "tile":3})
        elif mp[2]:
            self.p.send("CS_WSET", {"chunk":chunk, "tileref":tileref+(l,), "tile":0})
        elif mp[1]:
            self.p.send("CS_WSET", {"chunk":chunk, "tileref":tileref+(0,), "tile":4})

    def tick(self):

        self.world.update()
        self.entity_manager.update()

        if self.game.client.ticks-self.last_game_tick > self.ms_per_tick:

            self.handle_movement()

            self.last_game_tick = self.game.client.ticks

        if not self.ui.wman.windows:
            self.handle_wset()

        if self.player:
            cam_point = self.player.position if not self.moving else sum_coords(self.player.position, (0, self.view_bob*math.sin(self.game.client.ticks/self.view_bob_smooth)))
            self.scene.towards_camera(cam_point)