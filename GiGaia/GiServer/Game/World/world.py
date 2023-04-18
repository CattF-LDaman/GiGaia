
from GiGaia.GiCore.Game.World.Generation import Generator
from GiGaia.GiCore.Game.World.coords import coord_square, chunk_region

from GiGaia.GiServer.Data.worlddata import WorldData
from GiGaia.GiServer.Game.World.region import Region

class World:

    def __init__(self, game):
        
        self.game = game
        self.config = self.game.server.config.world

        self.name = self.config.name

        self.regions = {}

        self.data = WorldData(self.game.server.dirs["worlds"], self.name, self)
        self.seed = self.data.seed
        self.generator = Generator(self.data.seed, self.game.server.assets.TIDS, self.config.generator)
        self.generator.start()

    def serve(self, player):

        chunk_pos = player.entity.chunk_pos
        player_chunks = coord_square(chunk_pos, self.config.serve_range)
        served_chunks = []

        for c in player_chunks:
            cr = chunk_region(c)

            if cr not in self.regions:
                self.regions[cr] = Region(self, cr)

            if c not in self.regions[cr].chunks:
                self.regions[cr].create_chunk(c)

            if self.regions[cr].chunks[c].serve(player):
                served_chunks.append(c)

        return served_chunks