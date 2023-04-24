
from GiGaia.GiCore.Game.World import CHUNK_SIZE_TILES

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

    def generate(self):
        
        self.world.generator.generate_chunk(self.position)
    
    def set_at(self, x, y, z, tile_id):
        
        if not self.tiles:
            return

        if self.tiles[z][y][x] == tile_id:
            return
        
        self.tiles[z][y][x] = tile_id

        self.modifications.append({"chunk":self.position, "tileref":(x,y,z), "tile":tile_id})
        self.world.modified_chunks.append(self)

        self.modified = True

    def serve(self, player):

        if not self.tiles:
            self.tiles = self.world.generator.get_chunk(self.position)
        if not self.tiles:
            return False
        
        if self.position not in player.served_chunks:
            player.h.send("SC_CHUNK", {"position":self.position, "tiles":self.tiles})

        return True
