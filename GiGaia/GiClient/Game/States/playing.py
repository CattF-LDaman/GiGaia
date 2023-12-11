
from GiGaia.GiClient.Game.state import State
from GiGaia.GiClient.Game.Interfaces.playing import Playing as PlayingUI

from GiGaia.GiClient.Game.Entity.manager import EntityManager
from GiGaia.GiClient.Game.World.world import World
from GiGaia.GiClient.Game.scene import Scene
from GiGaia.GiClient.Game.World.lighting import LuxFlux
from GiGaia.GiClient.Game.States.Playing.inventory import PlayerInventory

from GiGaia.GiCore.Game.states import STATE_IDS as SIDS
from GiGaia.GiCore.Game.World.coords import pix_to_tileref, pix_to_tile, sum_coords, sub_coords

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

        self.selected_tile = 0  # SHOULD MOVE TO NEW CLASS.

        self.fullbright = False
        self.torch = False
        self.force_crash = False
        self.block_actions = False

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

        self.lux = LuxFlux(self)

    def handle_event(self, event):

        p = pygame.key.get_pressed()
        match event.type:
            case pygame.KEYDOWN:
                match event.key:

                    case pygame.K_F10:
                        self.game.log("Reloading chunk surfaces...")
                        for c in self.world.chunks.values():
                            c.draw_all()
                    case pygame.K_F5 if self.client.dev:
                        self.torch = not self.torch
                        self.game.log(f"Torch: {self.torch}")
                    case pygame.K_F9 if self.client.dev:
                        self.fullbright = not self.fullbright
                        self.game.log(f"Fullbright: {self.fullbright}")
                    case pygame.K_F11 if self.client.dev:
                        self.world.add_dev_light(self.scene.mouse)
                    case pygame.K_F4 if self.client.dev and pygame.key.get_pressed()[pygame.K_ESCAPE] and pygame.key.get_pressed()[pygame.K_END]:
                        self.client.log("Crashing game state...", 4)
                        self.force_crash = True
                    

                    case self.keybinds.CROUCH if p[self.keybinds.MOVE_DOWN]:
                        self.player.crouch(True)

            case pygame.KEYUP:
                match event.key:
                    case self.keybinds.CROUCH:
                        self.player.crouch(False) # Send crouch packet again to stop crouching
            case pygame.MOUSEWHEEL if self.ui.chat.chat_contents.auto_scroll and not self.ui.chat.chat_contents.hovered and not self.ui.wman.windows:
                tiles = self.game.assets.tiles
                if event.y > 0:
                    self.selected_tile = min(self.selected_tile+1,len(tiles))
                elif event.y < 0:
                    self.selected_tile = max(self.selected_tile-1,1)
                self.ui.chat.chat_in("GAME", f"TILE: {tiles[self.selected_tile].display_name}")

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

        if p[self.keybinds.MOVE_DOWN] or p[self.keybinds.CROUCH]:
            if self.player.props["flying"]:
                self.player.crouch(True)

    def handle_wset(self):  # Temporary

        l = 1 if pygame.key.get_pressed()[pygame.K_LSHIFT] else 0
        chunk, tileref = pix_to_tileref(self.scene.mouse)

        mp = pygame.mouse.get_pressed()
        if mp[0] and self.selected_tile:
            self.p.send("CS_WSET", {"chunk":chunk, "tileref":tileref+(l,), "tile":self.selected_tile})
        elif mp[2]:
            #self.p.send("CS_WSET", {"chunk":chunk, "tileref":tileref+(l,), "tile":0})
            self.p.send("CS_DESTROY", {"chunk":chunk, "tileref":tileref+(l,)})
        elif mp[1]: # tile picking
            mp_tile = pix_to_tile(self.scene.mouse)
            self.selected_tile = self.world.get_at(mp_tile[0], mp_tile[1], 0)
            if not self.selected_tile:
                self.selected_tile = self.world.get_at(mp_tile[0], mp_tile[1], 1)

            #self.p.send("CS_WSET", {"chunk":chunk, "tileref":tileref+(0,), "tile":4})

    def resize(self):

        self.lux.resize()

    def tick(self):

        if self.force_crash:
            raise RuntimeError("Goodbye! (Force crash triggered by ESCAPE + END + F4)")

        self.world.update()
        self.entity_manager.update()

        if not self.ui.chat.typing and not self.ui.wman.windows: # Actions disabled while typing chats or in windows go here

            if self.game.client.ticks-self.last_game_tick > self.ms_per_tick:

                self.handle_movement()

                self.last_game_tick = self.game.client.ticks

            if not self.ui.wman.windows and not (self.ui.game_menu and not self.ui.game_menu.deleted):
                self.handle_wset()

        if self.torch:
            self.lux.point_light(self.scene.mouse_screen, 200, (255,255,255))
        if not self.fullbright:
            self.lux.apply()

        if self.player:
            cam_point = self.player.position if not self.moving else sum_coords(self.player.position, (0, self.view_bob*math.sin(self.game.client.ticks/self.view_bob_smooth)))
            if pygame.key.get_pressed()[self.keybinds.FREELOOK]:
                cam_point = sub_coords(cam_point, sub_coords(self.game.screen.get_rect().center, self.scene.mouse_screen))
            self.scene.towards_camera(cam_point)