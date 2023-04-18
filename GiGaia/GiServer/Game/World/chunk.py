
from GiGaia.GiCore.Game.World import CHUNK_SIZE_TILES

class Chunk:

    def __init__(self, region, pos):

        self.region = region
        self.region_pos = region.position

        self.world = region.world
        self.position = pos

        #if don't have data banchood
        self.tiles = None
        self.generate()

        self.modifications = []
        self.tick = 0

    def generate(self):
        
        self.world.generator.generate_chunk(self.position)
    
    def set_at(self, x, y, z, tile_id):

        self.tiles[z][y][x] = tile_id
        self.modifications.append({"chunk":self.position, "tileref":(x,y,z), "tile":tile_id})

    def serve(self, player):

        if not self.tiles:
            self.tiles = self.world.generator.get_chunk(self.position)
        if not self.tiles:
            return False

        if self.tick != self.world.game.ticks:
            self.modifications = []
            self.tick = self.world.game.ticks
        
        if self.position not in player.served_chunks:
            player.h.send("SC_CHUNK", {"position":self.position, "tiles":self.tiles})
        elif len(self.modifications) > self.world.config.chunk_tile_mod_max:
            player.h.send("SC_UPDATE_CHUNK", {"chunk":self.position, "tiles":self.tiles})
        else:
            for mod in self.modifications:
                player.h.send("SC_UPDATE_TILE", mod)

        return True
