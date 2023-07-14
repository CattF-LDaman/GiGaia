
from GiGaia.GiCore.Game.World.coords import chunk_to_pix, mult_coord, tileref_to_tile, sum_coords, neighbours, tile_to_pix, tile_to_tileref
from GiGaia.GiCore.Game.World import CHUNKSURF_SIZE_PIXELS, CHUNK_SIZE_PIXELS, TILE_SPRITE_SIZE, CHUNK_SIZE_TILES, TILE_SIZE_PIXELS

import pygame

class Chunk:  # FUTURE: TILE UPDATES = LSIT OF ALL TIMES RANDOMLY POPPED UNTIL EMPTY THEN RESET

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

        self._lighting = pygame.Surface((CHUNK_SIZE_PIXELS, CHUNK_SIZE_PIXELS))
        self.lux = self.world.state.lux

        self.update_neighbours()

    @property
    def draw_pos(self):
        return self.world.scene.convert_world_to_screen_coord(self.world_position)

    def update_neighbours(self):
        for nb in neighbours(self.position):
            self.world.update_chunk((nb[0], nb[1]))

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
        for y, row in enumerate(layer):
            for x, tile in enumerate(row):
                if tile:
                    self.draw_tile(x, y, l, tile)

    def lit(self, x, y, strength=0, starter=None):

        # tpos = tileref_to_tile((self.position, (x,y)))

        # if starter == tpos:
        #     return 0

        # trbl = [self.world.get_at(*sum_coords(tpos, offset),1) for offset in ((0,-1),(1,0),(0,1),(-1,0))]

        # _highest_lit = 0

        # for rel_tile, offset in zip(trbl, ((0,-1),(1,0),(0,1),(-1,0))):
        #     if rel_tile is None:
        #         continue

        #     rel_tpos = sum_coords(tpos, offset)
        #     if rel_tpos != starter:
        #         return

        #     rel_chunk = self.world.get_chunk_at(*rel_tpos)
        #     if rel_chunk:
                
        #         if rel_tile == 0:
        #             _highest_lit = max(_highest_lit, self.lux.WORLD_LIGHT_LEVELS)
        #             continue
                
        #         if (rlit := rel_chunk.lit(*tile_to_tileref(rel_tpos)[1], starter or tpos)):
        #             _highest_lit = max(_highest_lit, rlit-1)

        # if _highest_lit:
        #     surf_tpos = mult_coord((x,y), TILE_SIZE_PIXELS)
        #     tr = pygame.Rect(surf_tpos[0], surf_tpos[1], TILE_SIZE_PIXELS, TILE_SIZE_PIXELS)
        #     pygame.draw.rect(self._lighting, (int(_highest_lit/self.lux.WORLD_LIGHT_LEVELS*255),)*3, tr)
        return
    
        tpos = tileref_to_tile((self.position, (x,y)))

        if tpos == starter:
            return

        if starter is None and self.tiles[1][y][x] == 0:
            strength = self.lux.WORLD_LIGHT_LEVELS
        # if self.tiles[1][y][x] == 0:
        #     strength = 5

        if strength:

            surf_tpos = mult_coord((x,y), TILE_SIZE_PIXELS)
            tr = pygame.Rect(surf_tpos[0], surf_tpos[1], TILE_SIZE_PIXELS, TILE_SIZE_PIXELS)
            #pygame.draw.rect(self._lighting, (int(strength/self.lux.WORLD_LIGHT_LEVELS*255),)*3, tr,)
            self._lighting.fill((int(strength/self.lux.WORLD_LIGHT_LEVELS*255),)*3, tr, pygame.BLEND_RGB_MAX)
        
            strength -= 1

            if strength:
                for offset in (((0,-1),(1,0),(0,1),(-1,0))):
                    relchunk, reltileref = self.world.get_tileref_at(*sum_coords(tpos, offset))
                    relchunk.lit(*reltileref, strength, starter or tpos)

    def draw_tile(self, x, y, l, tile):

        surf_tpos = mult_coord((x,y), TILE_SPRITE_SIZE)

        tr = pygame.Rect(surf_tpos[0], surf_tpos[1], TILE_SPRITE_SIZE, TILE_SPRITE_SIZE)
        pygame.draw.rect(self.surf_layers[l], (0,0,0), tr)

        if l == 1:
            self.lit(x, y)
            
        if not tile:
            return

        t_asset = self.assets.tiles[tile]
        tpos = tileref_to_tile((self.position, (x,y)))
        trand = hash(str(tpos))
        trbl = [self.world.get_at(*sum_coords(tpos, offset),l) for offset in ((0,-1),(1,0),(0,1),(-1,0))]

        # if l == 1:
        #     for rel_tile, offset in zip(trbl, ((0,-1),(1,0),(0,1),(-1,0))):
        #         if rel_tile == 0:
        #             rel_tpos = sum_coords(tpos, offset)
        #             rel_chunk = self.world.get_chunk_at(rel_tpos)
        #             if rel_chunk:

        #             # rel_center_px = sum_coords(tile_to_pix(rel_tpos), (int(TILE_SPRITE_SIZE/2), )*2)
        #             # self.lighting.append(rel_center_px)
        

        # pygame.draw.rect(self._lighting, (int(lit/self.lux.WORLD_LIGHT_LEVELS*255),)*3, tr)

        self.surf_layers[l].blit(t_asset.get_sprite(trbl, l, trand), surf_tpos)

    @property
    def lighting(self):

        lightsurf = pygame.Surface(self._lighting.get_size())
        lightsurf.fill(self.lux.natural_light)
        lightsurf.blit(self._lighting, (0,0), special_flags=pygame.BLEND_RGB_MULT)
        return lightsurf

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
            
            self.draw()

        elif self.updates:

            for x, y in self.updates:
                self.draw_tile(x, y, 1, self.tiles[1][y][x])
                self.draw_tile(x, y, 0, self.tiles[0][y][x])
            self.construct()

        self.updated = False
        self.updates.clear()

        return self.surface