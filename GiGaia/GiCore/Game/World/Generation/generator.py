from .Layers import SETTINGS as DEFAULT_SETTINGS
from .Layers import LAYERS

from GiGaia.GiCore.Game.World import CHUNK_SIZE_TILES
from GiGaia.GiCore.Game.World.coords import tileref_to_tile

import multiprocessing

GEN_Q_IN = 0
GEN_Q_OUT = 1

class Generator:

    def __init__(self, seed, tiles, structures, settings={}, generators=4):  # default arg is allowed to be mutable here bitch
        
        self.seed = seed
        self.settings = self.s = {**DEFAULT_SETTINGS, **settings}

        self.tiles = tiles  # AssetsManager.TIDS (SimpleNamespace)
        self.structures = structures # AssetsManager.STRUCTURES (SimpleNamespace)

        self.layers = [layer(self) for layer in LAYERS]

        # self.in_q = multiprocessing.Queue()
        # self.out_q = multiprocessing.Queue()
        self.generators = generators
        self.generator_queues = [(multiprocessing.Queue(), multiprocessing.Queue()) for g in range(generators)]

        self.generating = 0

        self.cur_selected = 0

        self.storage = {}

    def start(self):

        for generator_num in range(self.generators):
            multiprocessing.Process(target=self.generator, args=(generator_num,), name=f"GiGaiaGen{generator_num}", daemon=True).start()

    def generate_chunk(self, chunk_pos):

        self.generator_queues[self.cur_selected][GEN_Q_IN].put(chunk_pos)
        self.generating += 1
        self.cur_selected += 1
        if self.cur_selected >= self.generators:
            self.cur_selected = 0

    def generator(self, gen_num):

        while True:

            chunk_pos = self.generator_queues[gen_num][GEN_Q_IN].get()

            tiledata = []
            for z in range(2):
                tiledata.append([])
                for y in range(CHUNK_SIZE_TILES):
                    tiledata[z].append([])
                    for x in range(CHUNK_SIZE_TILES):
                            wx, wy = tileref_to_tile((chunk_pos, (x,y)))
                            tiledata[z][y].append(self.get_at(wx, wy ,z))

            self.generator_queues[gen_num][GEN_Q_OUT].put((chunk_pos, tiledata))

    def fetch_ready(self):

        for gen in self.generator_queues:
            out_queue = gen[GEN_Q_OUT]
            while not out_queue.empty():
                cp, tiles = out_queue.get()
                self.storage[cp] = tiles
                self.generating -= 1

    def get_chunk(self, chunk_pos):

        self.fetch_ready()

        if chunk_pos in self.storage:
            return self.storage.pop(chunk_pos)

    def get_at(self, x, y, z):

        tile = 0
        for l in self.layers:

            tile = l.get_at(x, y, z, tile)

        return tile