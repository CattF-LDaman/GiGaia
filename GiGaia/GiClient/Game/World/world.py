
from .chunk import Chunk
from GiGaia.GiCore.Game.World.coords import pix_to_chunk, coord_range, coord_square, add_coord, tile_to_tileref
from GiGaia.GiCore.Game.World.timestamp import Timestamp
from GiGaia.GiCore.Game.World import TILE_SPRITE_SIZE, DARK_COMPLETE_DEPTH, DARKER_FROM_DEPTH, HORIZON, COMPLETE_DARKNESS
from GiGaia.GiCore.color_util import mult_color

import time
import math
import random
import pygame
from functools import lru_cache

class World:
        
    def __init__(self, state):
        
        self.state = state
        self.scene = state.scene
        self.p = state.p
        self.game = state.game
        self.assets = state.game.assets
        self.config = state.game.config.world

        self.chunks = {}
        
        self.tile_updates = 0
        self.viewport_size = 0

        self._time_reference = [0, 0] # IN-GAME, MONOTONIC

        self.daycycle = self.assets.data.daycycle

        self.p.hold_all("SC_CHUNK","SC_UPDATE_TILE","SC_UPDATE_CHUNK")
        self.p.subscribe("SC_TIME", self.update_time)

        self.dev_lights = []
        self.dev_light_color_base = (255, 113, 61)
        self.dev_light_radius = 200
        self.dev_light_intensity = 2

    def dev_light_color(self, brightness): # brightness: 0-20
        return mult_color(self.dev_light_color_base, int(brightness)/20)

    def add_dev_light(self, loc):

        self.dev_lights.append([loc, 1])

    def create_chunk(self, chunk_pos, tiles):

        self.chunks[chunk_pos] = Chunk(self, chunk_pos, tiles)

    def update_time(self, tp):

        self._time_reference[1] = time.monotonic()
        self._time_reference[0] = tp.time

    @property
    def time_value(self):

        return self._time_reference[0] + (time.monotonic() - self._time_reference[1])

    @property
    def time(self):

        return Timestamp(self.time_value)

    def get_at(self, x,y,z):
        chunk, tileref = tile_to_tileref((x,y))
        if chunk not in self.chunks:
            return 0

        return self.chunks[chunk].tiles[z][tileref[1]][tileref[0]]
    
    def get_tileref_at(self, x, y):
        chunk, tileref = tile_to_tileref((x,y))
        if chunk not in self.chunks:
            return None

        return self.chunks[chunk], tileref

    def update_tile(self, x, y):
        chunk, tileref = tile_to_tileref((x,y))
        if chunk not in self.chunks:
            return
        
        self.chunks[chunk].update_tile(*tileref)

    def update_chunk(self, chunk_pos):
        if chunk_pos in self.chunks:
            self.chunks[chunk_pos].draw_all()

    def handle_packets(self):

        for cp in self.p.fetch("SC_CHUNK"):
            if cp.position not in self.chunks:
                self.create_chunk(cp.position, cp.tiles)
            else:
                self.chunks[cp.position].set_all(cp.tiles)

        for utp in self.p.fetch("SC_UPDATE_TILE"):
            if utp.chunk in self.chunks:
                self.chunks[utp.chunk].set_tile(utp.tileref, utp.tile)

        for ucp in self.p.fetch("SC_UPDATE_CHUNK"):
            if ucp.chunk in self.chunks:
                self.chunks[ucp.chunk].set_all(ucp.tiles)

    def get_viewport_chunks(self, padding=0):
        
        topleft = self.scene.convert_screen_to_world_coord(add_coord((0,0), -padding))
        botright = self.scene.convert_screen_to_world_coord(add_coord(self.game.screen.get_size(), padding))

        #topleft = (self.state.scene.camera_pos[0]-self.game.screen.get_width()/2,self.state.scene.camera_pos[1]-self.game.screen.get_height()/2)
        #botright = (self.state.scene.camera_pos[0]+self.game.screen.get_width()/2,self.state.scene.camera_pos[1]+self.game.screen.get_height()/2)

        return coord_range(pix_to_chunk(topleft), pix_to_chunk(botright, ceil=True)) #coord_square(pix_to_chunk(self.scene.camera_pos), 4)

    @property
    def camera_depth(self):

        return self.scene.camera_pos[1] - HORIZON

    @property
    def sky_color(self):

        if self.camera_depth > DARKER_FROM_DEPTH:
            difference = self.camera_depth - DARKER_FROM_DEPTH
            ratio = difference / DARK_COMPLETE_DEPTH
            depth_mult = max(1-min(ratio, 1), COMPLETE_DARKNESS)
        else:
            depth_mult = 1

        return mult_color(self.time.sky_color(self.daycycle), depth_mult)

    def draw(self):

        self.game.screen.fill(self.sky_color)

        viewport_chunks = self.get_viewport_chunks()  # These are actually drawn to screen
        padded_viewport_chunks = self.get_viewport_chunks(self.config.viewport_padding)  # Used for chunk updates

        self.tile_updates = 0
        self.viewport_size = len(viewport_chunks)

        viewport_surfs = []

        if (player_ent := self.state.player): # prioritize player chunk
            player_chunk_pos = player_ent.chunk_pos
            player_chunk = self.chunks[player_chunk_pos]
            if (chunk_surface := player_chunk.get_surface()):
                viewport_surfs.append((chunk_surface, player_chunk.draw_pos))

        for cp in padded_viewport_chunks:

            if cp in self.chunks and cp != player_chunk_pos:

                c = self.chunks[cp]

                if (chunk_surface := c.get_surface()) and cp in viewport_chunks:
                    viewport_surfs.append((chunk_surface, c.draw_pos))

        self.game.screen.fblits(viewport_surfs)

        self.handle_dev_lights()

    def handle_dev_lights(self):

        for dl in self.dev_lights:
            dl[1] = max(min(dl[1]+math.sin(dl[1]+dl[0][0]+self.time_value*10)*random.uniform(0.8,0.1), 20), 15)
            self.state.lux.point_light(dl_p := self.scene.convert_world_to_screen_coord(dl[0]), self.state.world.dev_light_radius, self.dev_light_color(dl[1]), self.dev_light_intensity)
            dl_rect = pygame.Rect(0, 0, dl[1]//2, dl[1]//2)
            dl_rect.center = dl_p
            pygame.draw.rect(self.state.lux.lit_up_surface, self.dev_light_color_base, dl_rect)

    def update(self):

        self.handle_packets()
        self.draw()
