
from GiGaia.GiCore.Game.World.coords import chunk_to_pix, mult_coord
from GiGaia.GiCore.Game.World import CHUNKSURF_SIZE_PIXELS, CHUNK_SIZE_PIXELS, TILE_SPRITE_SIZE

import pygame

class Chunk:

    def __init__(self, world, position, tiles):
        
        self.world = world
        self.assets = self.world.assets
        self.position = position
        self.world_position = chunk_to_pix(self.position)

        self.tiles = tiles

        self._surface = pygame.Surface((CHUNKSURF_SIZE_PIXELS, CHUNKSURF_SIZE_PIXELS))
        self.surface = None
        self.updated = True

    def set_tile(self, tr, tile):

        self.tiles[tr.z][tr.y][tr.x] = tile
        self.updated = True

    def set_all(self, tiles):
        
        self.tiles = tiles
        self.updated = True

    def draw_layer(self, l, layer):
        for y, row in enumerate(layer):
            for x, tile in enumerate(row):
                if tile:
                    t_asset = self.assets.tiles[tile]
                    self._surface.blit(t_asset.get_sprite(l), mult_coord((x,y), TILE_SPRITE_SIZE))

    def get_surface(self):
        
        if self.updated:
            
            self.world.surface_updates += 1
            self._surface.fill((0,0,0))
            for rl, layer in enumerate(self.tiles[::-1]):
                self.draw_layer(1-rl, layer)
            self.surface = pygame.transform.scale(self._surface, (CHUNK_SIZE_PIXELS, CHUNK_SIZE_PIXELS))

        self.updated = False

        return self.surface