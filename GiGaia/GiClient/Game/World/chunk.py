
from GiGaia.GiCore.Game.World.coords import chunk_to_pix, mult_coord, tileref_to_tile, sum_coords, neighbours
from GiGaia.GiCore.Game.World import CHUNKSURF_SIZE_PIXELS, CHUNK_SIZE_PIXELS, TILE_SPRITE_SIZE, CHUNK_SIZE_TILES, TILE_SIZE_PIXELS
from GiGaia.GiCore.sprite_util import flat_square

import pygame
import collections

class Chunk:  # FUTURE: TILE UPDATES = LSIT OF ALL TIMES RANDOMLY POPPED UNTIL EMPTY THEN RESET

    MISSING_TILE = flat_square((255,50,255), TILE_SPRITE_SIZE)

    def __init__(self, world, position, tiles):
        
        self.world = world
        self.assets = self.world.assets
        self.position = position
        self.world_position = chunk_to_pix(self.position)

        self.tiles = tiles

        self._surface = pygame.Surface((CHUNKSURF_SIZE_PIXELS, CHUNKSURF_SIZE_PIXELS))
        self._surface.set_colorkey((0,0,0))
        self.surf_layers = [self._surface.copy(), self._surface.copy()]
        self.surface = None
        self.tile_updates = collections.deque()
        self.draw_all()

        self.update_neighbours()

    @property
    def draw_pos(self):
        return self.world.scene.convert_world_to_screen_coord(self.world_position)

    def draw_all(self):
        for l, layer in enumerate(self.tiles[::-1]):
            for y, row in enumerate(layer):
                for x, tile in enumerate(row):
                    if tile:
                        self.tile_updates.append([x, y, 1-l, tile])

    def update_neighbours(self):

        def update_tile_nb(x, y):
            tile_pos = tileref_to_tile((self.position, (x, y)))
            for nb in neighbours(tile_pos):
                self.world.update_tile(*nb)

        for y in (0, CHUNK_SIZE_TILES-1):
            for x in range(CHUNK_SIZE_TILES):
                update_tile_nb(x, y)
                
        for x in (0, CHUNK_SIZE_TILES-1):
            for y in range(CHUNK_SIZE_TILES):
                update_tile_nb(x, y)

    def set_tile(self, tr, tile):

        self.tiles[tr.z][tr.y][tr.x] = tile
        self.update_tile(tr.x, tr.y)

        tile_pos = tileref_to_tile((self.position, (tr.x, tr.y)))
        for nb in neighbours(tile_pos):
            self.world.update_tile(*nb)

    def set_all(self, tiles):
        
        self.tiles = tiles
        self.draw_all()
        self.update_neighbours()

    def draw_tile(self, x, y, l, tile, blit_later=False):

        surf_tpos = mult_coord((x,y), TILE_SPRITE_SIZE)

        tr = pygame.Rect(surf_tpos[0], surf_tpos[1], TILE_SPRITE_SIZE, TILE_SPRITE_SIZE)
        pygame.draw.rect(self.surf_layers[l], (0,0,0), tr)

        if not tile:
            ts = pygame.Surface((TILE_SPRITE_SIZE, TILE_SPRITE_SIZE))
            ts.fill((0,0,0))
            return (ts, surf_tpos)

        try:
            t_asset = self.assets.tiles[tile]
            tpos = tileref_to_tile((self.position, (x,y)))
            trand = hash(str(tpos))
            trbl = [self.world.get_at(*sum_coords(tpos, offset),l) for offset in ((0,-1),(1,0),(0,1),(-1,0))]

            if blit_later:
                return (t_asset.get_sprite(trbl, l, trand), surf_tpos)

            self.surf_layers[l].blit(t_asset.get_sprite(trbl, l, trand), surf_tpos)
        except KeyError:
            if blit_later:
                return (Chunk.MISSING_TILE, surf_tpos)
            pygame.draw.rect(self.surf_layers[l], (255,50,255), tr) # Missing tile

    def draw_amount(self, amount=1):
        draws = [[],[]]
        amount = min(amount, len(self.tile_updates))
        for _ in range(amount):
            x, y, l, tile = self.tile_updates.popleft()
            if (draw_tile := self.draw_tile(x, y, l, tile, blit_later=True)) is not None:
                draws[l].append(draw_tile)
        for dl in range(2):
            self.surf_layers[dl].fblits(draws[dl])
        if not self.tile_updates:
            self.construct()
        self.world.tile_updates += amount

    def construct(self):

        self._surface = pygame.Surface((CHUNKSURF_SIZE_PIXELS, CHUNKSURF_SIZE_PIXELS))
        self._surface.set_colorkey((0,0,0))
        for lsurf in self.surf_layers[::-1]:
            self._surface.blit(lsurf, (0,0))
        self.surface = pygame.transform.scale(self._surface, (CHUNK_SIZE_PIXELS, CHUNK_SIZE_PIXELS))

    def update_tile(self, x, y, l=None):

        if l is not None:
            self.tile_updates.append([x, y, l, self.tiles[l][y][x]])
        else:
            self.tile_updates.append([x, y, 1, self.tiles[1][y][x]])
            self.tile_updates.append([x, y, 0, self.tiles[0][y][x]])

    def get_surface(self):
        
        if self.tile_updates and self.world.tile_updates < self.world.game.config.world.max_tile_updates_per_tick:
            
            amount = self.world.game.config.world.max_tile_updates_per_tick - self.world.tile_updates
            self.draw_amount(amount)

        return self.surface