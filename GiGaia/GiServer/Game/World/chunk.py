
from GiGaia.GiCore.Game.World import TILE_SIZE_PIXELS, CHUNK_SIZE_PIXELS, CHUNK_SIZE_TILES

import pygame

class Chunk:

    def __init__(self, region, pos):

        self.region = region
        self.region_pos = region.position

        self.world = region.world
        self.position = pos

        self.tiles = self.world.data.get_chunk(self.position)
        if not self.tiles:
            self.generate()

        self.observers = []
        self.modifications = []
        self.modified = False  # Used to check whether to save chunk, gets reset on save.
        self.tick = 0

        self._collision = []

    def generate(self):
        
        self.world.generator.generate_chunk(self.position)
    
    def get_collision(self):

        if not self._collision and self.tiles:

            for y, row in enumerate(self.tiles[0]):

                row_rects = []
                tr = pygame.Rect(0,0,0,0)
                tr.topleft = (0,y*TILE_SIZE_PIXELS)
                tr.height = TILE_SIZE_PIXELS

                for x, tile in enumerate(row):

                    if tile != 0:

                        tr.width = tr.width + TILE_SIZE_PIXELS

                    else:

                        if tr.width >= TILE_SIZE_PIXELS:
                            tr.topleft = (self.position[0]*CHUNK_SIZE_PIXELS+tr.topleft[0],self.position[1]*CHUNK_SIZE_PIXELS+tr.topleft[1])
                            row_rects.append(tr.copy())

                        tr.topleft = (tr.topleft[0] + TILE_SIZE_PIXELS,tr.topleft[1])
                        tr.width = 0

                    if x == CHUNK_SIZE_TILES-1 and tr.width>0:
                        tr.topleft = (self.position[0]*CHUNK_SIZE_PIXELS+tr.topleft[0],self.position[1]*CHUNK_SIZE_PIXELS+tr.topleft[1])
                        row_rects.append(tr.copy())

                self._collision.extend(row_rects)

        return self._collision

    def set_at(self, x, y, z, tile_id):
        
        if not self.tiles:
            return

        if self.tiles[z][y][x] == tile_id:
            return
        
        self.tiles[z][y][x] = tile_id

        self.modifications.append({"chunk":self.position, "tileref":(x,y,z), "tile":tile_id})
        self.world.modified_chunks.append(self)

        self.modified = True
        self._collision.clear()  # Collision rects need to be regenerated

    def serve(self, player):

        if not self.tiles:
            self.tiles = self.world.generator.get_chunk(self.position)
        if not self.tiles:
            return False
        
        if self.position not in player.served_chunks:
            player.h.send("SC_CHUNK", {"position":self.position, "tiles":self.tiles})

        return True
