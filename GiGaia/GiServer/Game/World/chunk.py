
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

        #self.modifications = []
        self.observers = []
        self.modified = False  # Used to check wether to save chunk, gets reset on save.
        self.tick = 0

    def generate(self):
        
        self.world.generator.generate_chunk(self.position)
    
    def set_at(self, x, y, z, tile_id):
        
        if not self.tiles:
            return

        self.tiles[z][y][x] = tile_id
        #self.modifications.append({"chunk":self.position, "tileref":(x,y,z), "tile":tile_id})
        for player in self.observers:
            player.h.send("SC_UPDATE_TILE",{"chunk":self.position, "tileref":(x,y,z), "tile":tile_id})
        self.modified = True

    def serve(self, player):

        if not self.tiles:
            self.tiles = self.world.generator.get_chunk(self.position)
        if not self.tiles:
            return False

        # if self.tick != self.world.game.ticks:
        #     self.modifications = []
        #     self.tick = self.world.game.ticks

        if self.tick != self.world.game.ticks:
            self.observers = []
            self.tick = self.world.game.ticks

        if self.position not in player.served_chunks:
            player.h.send("SC_CHUNK", {"position":self.position, "tiles":self.tiles})
        # elif len(self.modifications) > self.world.config.chunk_tile_mod_max:
        #     player.h.send("SC_UPDATE_CHUNK", {"chunk":self.position, "tiles":self.tiles})
        # else:
        #     for mod in self.modifications:
        #         player.h.send("SC_UPDATE_TILE", mod)

        return True
