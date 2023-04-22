
from GiGaia.GiCore.Game.World.Generation import Generator
from GiGaia.GiCore.Game.World.coords import coord_square, chunk_region, tile_to_chunk
from GiGaia.GiCore.threading import threaded_nondaemon

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

        self.last_save = 0

    @property
    def should_save(self):

        return self.game.ticks - self.last_save > 1000

    @threaded_nondaemon
    def save(self):

        self.last_save = self.game.ticks
        self.data.save()

    def get_chunk(self, cp):

        cr = chunk_region(cp)

        if cr not in self.regions:
            self.create_region(cr)

        if cp not in self.regions[cr].chunks:
            self.regions[cr].create_chunk(cp)

        return self.regions[cr].chunks[cp]

    def create_region(self, rp):

        self.regions[rp] = Region(self, rp)

    def grab_chunk(self, cp):

        return self.regions[chunk_region(cp)].chunks[cp]

    def serve(self, player):

        chunk_pos = player.entity.chunk_pos
        player_chunks = coord_square(chunk_pos, self.config.serve_range)
        served_chunks = []

        for c in player_chunks:

            chunk = self.get_chunk(c)
            if chunk.serve(player):
                served_chunks.append(c)

        return served_chunks