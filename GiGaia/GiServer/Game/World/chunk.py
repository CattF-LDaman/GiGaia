
from GiGaia.GiCore.Game.World import CHUNK_SIZE_TILES

class Chunk:

    def __init__(self, region, pos):

        self.region = region
        self.region_pos = region.position

        self.world = region.world
        self.position = pos

        #if don't have data banchood
        self.tiles = self.generate()

        self.modifications = []
        self.tick = 0

    def generate(self):
        
        gen = self.world.generator
        tiledata = []
        for z in range(2):
            tiledata.append([])
            for y in range(CHUNK_SIZE_TILES):
                tiledata[z].append([])
                for x in range(CHUNK_SIZE_TILES):
                        tiledata[z][y].append(gen.get_at(x, y ,z))

        return tiledata
    
    def set_at(self, x, y, z, tile_id):

        self.tiles[z][y][x] = tile_id
        self.modifications.append({"chunk":self.position, "tileref":(x,y,z), "tile":tile_id})

    def serve(self, player):

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
