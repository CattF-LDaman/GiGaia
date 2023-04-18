
from .chunk import Chunk
from GiGaia.GiCore.Game.World.coords import pix_to_chunk, coord_range, coord_square, add_coord

from functools import lru_cache

class World:
        
    def __init__(self, state):
        
        self.state = state
        self.scene = state.scene
        self.p = state.p
        self.game = state.game
        self.assets = state.game.assets

        self.chunks = {}

        self.p.hold_all("SC_CHUNK","SC_UPDATE_TILE","SC_UPDATE_CHUNK")

    def create_chunk(self, chunk_pos, tiles):

        self.chunks[chunk_pos] = Chunk(self, chunk_pos, tiles)

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

        return coord_range(add_coord(pix_to_chunk(topleft),-1), add_coord(pix_to_chunk(botright),1)) #coord_square(pix_to_chunk(self.scene.camera_pos), 4)

    def draw(self):

        for cp in self.get_viewport_chunks():

            if cp in self.chunks:

                c = self.chunks[cp]
                self.game.screen.blit(c.get_surface(), self.scene.convert_world_to_screen_coord(c.world_position))

    def update(self):

        self.handle_packets()
        self.draw()
