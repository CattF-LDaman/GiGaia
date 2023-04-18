from .Layers import SETTINGS as DEFAULT_SETTINGS
from .Layers import LAYERS

from GiGaia.GiCore.Game.World import CHUNK_SIZE_TILES
from GiGaia.GiCore.Game.World.coords import tileref_to_tile

import multiprocessing

class Generator:

    def __init__(self, seed, tiles, settings={}):  # default arg is allowed to be mutable here bitch
        
        self.seed = seed
        self.settings = self.s = {**DEFAULT_SETTINGS, **settings}

        self.tiles = tiles  # AssetsManager.TIDS (SimpleNamespace)

        self.layers = [layer(self) for layer in LAYERS]

        self.in_q = multiprocessing.Queue()
        self.out_q = multiprocessing.Queue()

        self.storage = {}

    def start(self):

        self.process = multiprocessing.Process(target=self.generator, name="GiGaiaGenerator", daemon=True)
        self.process.start()

    def generate_chunk(self, chunk_pos):

        self.in_q.put(chunk_pos)

    def generator(self):

        while True:

            chunk_pos = self.in_q.get()

            tiledata = []
            for z in range(2):
                tiledata.append([])
                for y in range(CHUNK_SIZE_TILES):
                    tiledata[z].append([])
                    for x in range(CHUNK_SIZE_TILES):
                            wx, wy = tileref_to_tile((chunk_pos, (x,y)))
                            tiledata[z][y].append(self.get_at(wx, wy ,z))

            self.out_q.put((chunk_pos, tiledata))

    def get_chunk(self, chunk_pos):

        while not self.out_q.empty():
            cp, tiles = self.out_q.get()
            self.storage[cp] = tiles

        if chunk_pos in self.storage:
            return self.storage.pop(chunk_pos)

    def get_at(self, x, y, z):

        tile = 0
        for l in self.layers:

            tile = l.get_at(x, y, z, tile)

        return tile