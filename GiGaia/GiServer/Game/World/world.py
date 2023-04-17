
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

    def serve(self, player):

        chunk_pos = player.entity.chunk_pos
        served_chunks = coord_square(chunk_pos, self.config.serve_range)

        for c in served_chunks:
            cr = chunk_region(c)

            if cr not in self.regions:
                self.regions[cr] = Region(self, cr)

            if c not in self.regions[cr].chunks:
                self.regions[cr].create_chunk(c)

            self.regions[cr].chunks[c].serve(player)

        return served_chunks