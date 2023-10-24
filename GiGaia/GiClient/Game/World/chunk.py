
from GiGaia.GiCore.Game.World.coords import chunk_to_pix, mult_coord, tileref_to_tile, sum_coords, neighbours
from GiGaia.GiCore.Game.World import CHUNKSURF_SIZE_PIXELS, CHUNK_SIZE_PIXELS, TILE_SPRITE_SIZE, CHUNK_SIZE_TILES, TILE_SIZE_PIXELS
from GiGaia.GiCore.sprite_util import flat_square

import pygame

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

        self.updated = True
        self.updates = []

        self.update_neighbours()

    @property
    def draw_pos(self):
        return self.world.scene.convert_world_to_screen_coord(self.world_position)

    def update_neighbours(self):
        # for nb in neighbours(self.position):
        #     self.world.update_chunk((nb[0], nb[1]))
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
        self.updated = True
        self.update_neighbours()

    def draw_layer(self, l, layer):
        tile_draws = []
        for y, row in enumerate(layer):
            for x, tile in enumerate(row):
                if tile:
                    tile_draws.append(self.draw_tile(x, y, l, tile, blit_later=True))
        self.surf_layers[l].blits(tile_draws)

    def draw_tile(self, x, y, l, tile, blit_later=False):

        surf_tpos = mult_coord((x,y), TILE_SPRITE_SIZE)

        tr = pygame.Rect(surf_tpos[0], surf_tpos[1], TILE_SPRITE_SIZE, TILE_SPRITE_SIZE)
        pygame.draw.rect(self.surf_layers[l], (0,0,0), tr)

        if not tile:
            return

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

    def draw(self):
        self.world.surface_updates += 1
        self._surface.fill((0,0,0))
        for rl, layer in enumerate(self.tiles[::-1]):
            self.surf_layers[1-rl].fill((0,0,0))
            self.draw_layer(1-rl, layer)
        self.construct()

    def construct(self):

        self._surface = pygame.Surface((CHUNKSURF_SIZE_PIXELS, CHUNKSURF_SIZE_PIXELS))
        self._surface.set_colorkey((0,0,0))
        for lsurf in self.surf_layers[::-1]:
            self._surface.blit(lsurf, (0,0))
        self.surface = pygame.transform.scale(self._surface, (CHUNK_SIZE_PIXELS, CHUNK_SIZE_PIXELS))

    def update_tile(self, x, y):

        self.updates.append((x,y))

    def get_surface(self):
        
        if self.updated:
            
            if self.world.surface_updates < self.world.game.config.world.max_chunk_updates_per_tick:
                self.draw()
            else:
                return None

        elif self.updates:

            for x, y in self.updates:
                self.draw_tile(x, y, 1, self.tiles[1][y][x])
                self.draw_tile(x, y, 0, self.tiles[0][y][x])
            self.construct()

        self.updated = False
        self.updates.clear()

        return self.surface