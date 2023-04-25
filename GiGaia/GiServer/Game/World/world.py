
from GiGaia.GiCore.Game.World.Generation import Generator
from GiGaia.GiCore.Game.World.coords import coord_square, chunk_region, tile_to_chunk
from GiGaia.GiCore.Game.World.timestamp import Timestamp
from GiGaia.GiCore.threading import threaded_nondaemon

from GiGaia.GiServer.Data.worlddata import WorldData
from GiGaia.GiServer.Game.World.region import Region

import time

class World:

    def __init__(self, game):
        
        self.game = game
        self.config = self.game.server.config.world

        self.name = self.config.name

        self.regions = {}
        self.modified_chunks = []

        self.data = WorldData(self.game.server.dirs["worlds"], self.name, self)
        self.seed = self.data.seed
        self.generator = Generator(self.data.seed, self.game.server.assets.TIDS, self.config.generator)
        self.generator.start()

        self.last_save = 0
        self.last_time_upd = 0

        self.time_start = self.data.game_time
        self.time_ref = time.monotonic()

    @property
    def should_save(self):

        return self.game.ticks - self.last_save > 1000

    @property
    def should_update_time(self):
        
        return self.game.ticks - self.last_time_upd > 10000

    @property
    def time(self):

        return Timestamp(self.time_start + (time.monotonic()-self.time_ref))

    @threaded_nondaemon
    def save(self):

        self.last_save = self.game.ticks
        self.data.save()

    def update_time(self):

        self.game.traffic.broadcast("SC_TIME", {"time":self.time.value})
        self.last_time_upd = self.game.ticks

    def update_time_player(self, player):

        player.h.send("SC_TIME", {"time":self.time.value})

    def unload(self):

        for r in self.regions.copy().values():
            for chunk in r.chunks.copy().values():
                if not chunk.observers and not chunk.modified:
                    r.chunks.pop(chunk.position)
            if not r.chunks:
                self.regions.pop(r.position)

    def get_chunk(self, cp):

        cr = chunk_region(cp)

        if cr not in self.regions:
            self.create_region(cr)

        if cp not in self.regions[cr].chunks:
            self.regions[cr].create_chunk(cp)

        return self.regions[cr].chunks[cp]
    
    def has_chunk(self, cp):

        if chunk_region(cp) not in self.regions:
            return False
        
        if cp not in self.regions[chunk_region(cp)].chunks:
            return False
        
        return True

    def grab_any(self,chunks):

        return [self.grab_chunk(cp) for cp in chunks if self.has_chunk(cp)]

    def create_region(self, rp):

        self.regions[rp] = Region(self, rp)

    def grab_chunk(self, cp):

        return self.regions[chunk_region(cp)].chunks[cp]

    def tick(self):
    
        if self.should_save:
            self.save()
            # self.world.unload() # KANKER KANKER KUT KANKER ZOOI VUILE KANKER FLIKKER

        if self.should_update_time:
            self.update_time()

        self.handle_modifications()

    def handle_modifications(self):

        for chunk in self.modified_chunks:
            for player in chunk.observers:
                player.world_updates[chunk.position] = chunk.modifications
            chunk.observers.clear()
        self.modified_chunks.clear()

    def serve(self, player):

        chunk_pos = player.entity.chunk_pos
        player_chunks = coord_square(chunk_pos, self.config.serve_range)
        served_chunks = []

        for c in player_chunks:

            chunk = self.get_chunk(c)
            if chunk.serve(player):
                served_chunks.append(c)

        return served_chunks