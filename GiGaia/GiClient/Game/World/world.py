
from .chunk import Chunk
from GiGaia.GiCore.Game.World.coords import pix_to_chunk, coord_range, coord_square, add_coord, tile_to_tileref
from GiGaia.GiCore.Game.World.timestamp import Timestamp
from GiGaia.GiCore.Game.World import TILE_SPRITE_SIZE, DARK_COMPLETE_DEPTH, DARKER_FROM_DEPTH, HORIZON, COMPLETE_DARKNESS
from GiGaia.GiCore.color_util import mult_color

import time
import pygame
from functools import lru_cache

class World:
        
    def __init__(self, state):
        
        self.state = state
        self.scene = state.scene
        self.p = state.p
        self.game = state.game
        self.assets = state.game.assets

        self.chunks = {}
        
        self.surface_updates = 0
        self.viewport_size = 0

        self._time_reference = [0, 0] # IN-GAME, MONOTONIC

        self.daycycle = self.assets.data.daycycle

        self.p.hold_all("SC_CHUNK","SC_UPDATE_TILE","SC_UPDATE_CHUNK")
        self.p.subscribe("SC_TIME", self.update_time)

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
            self.chunks[chunk_pos].updated = True

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

    def get_viewport_chunks(self):
        
        topleft = self.scene.convert_screen_to_world_coord((0,0))
        botright = self.scene.convert_screen_to_world_coord(self.game.screen.get_size())

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

        viewport_chunks = self.get_viewport_chunks()

        self.surface_updates = 0
        self.viewport_size = len(viewport_chunks)

        for cp in viewport_chunks:

            if cp in self.chunks:

                c = self.chunks[cp]

                if (chunk_surface := c.get_surface()):
                    self.game.screen.blit(chunk_surface, c.draw_pos)
                #self.state.lux.free_light(c.lighting, c.draw_pos)

    def update(self):

        self.handle_packets()
        self.draw()
