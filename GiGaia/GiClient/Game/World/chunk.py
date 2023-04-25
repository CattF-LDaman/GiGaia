
from GiGaia.GiCore.Game.World.coords import chunk_to_pix, mult_coord, tileref_to_tile, sum_coords
from GiGaia.GiCore.Game.World import CHUNKSURF_SIZE_PIXELS, CHUNK_SIZE_PIXELS, TILE_SPRITE_SIZE, CHUNK_SIZE_TILES

import pygame

class Chunk:

    def __init__(self, world, position, tiles):
        
        self.world = world
        self.assets = self.world.assets
        self.position = position
        self.world_position = chunk_to_pix(self.position)

        self.tiles = tiles

        self._surface = pygame.Surface((CHUNKSURF_SIZE_PIXELS, CHUNKSURF_SIZE_PIXELS))
        self._surface.set_colorkey((0,0,0))
        self.surface = None
        self.updated = True

        self.update_neighbours()

    def update_neighbours(self):
        self.world.update_chunk((self.position[0], self.position[1]-1))
        self.world.update_chunk((self.position[0], self.position[1]+1))
        self.world.update_chunk((self.position[0]-1, self.position[1]))
        self.world.update_chunk((self.position[0]+1, self.position[1]))

    def set_tile(self, tr, tile):

        self.tiles[tr.z][tr.y][tr.x] = tile

        cp = self.position
        if tr.y == 0:
            self.world.update_chunk((cp[0], cp[1]-1))
        elif tr.y == CHUNK_SIZE_TILES-1:
            self.world.update_chunk((cp[0], cp[1]+1))

        if tr.x == 0:
            self.world.update_chunk((cp[0]-1, cp[1]))
        elif tr.x == CHUNK_SIZE_TILES-1:
            self.world.update_chunk((cp[0]+1, cp[1]))

        self.updated = True

    def set_all(self, tiles):
        
        self.tiles = tiles
        self.updated = True
        self.update_neighbours()

    def draw_layer(self, l, layer):
        for y, row in enumerate(layer):
            for x, tile in enumerate(row):
                if tile:
                    t_asset = self.assets.tiles[tile]
                    tpos = tileref_to_tile((self.position, (x,y)))
                    trand = hash(str(tpos))
                    trbl = [self.world.get_at(*sum_coords(tpos, offset),l) for offset in ((0,-1),(1,0),(0,1),(-1,0))]
                    self._surface.blit(t_asset.get_sprite(trbl, l, trand), mult_coord((x,y), TILE_SPRITE_SIZE))

    def get_surface(self):
        
        if self.updated:
            
            self.world.surface_updates += 1
            self._surface.fill((0,0,0))
            for rl, layer in enumerate(self.tiles[::-1]):
                self.draw_layer(1-rl, layer)
            self.surface = pygame.transform.scale(self._surface, (CHUNK_SIZE_PIXELS, CHUNK_SIZE_PIXELS))

        self.updated = False

        return self.surface