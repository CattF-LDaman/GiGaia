
from types import SimpleNamespace

class Layer:

    def __init__(self, generator):
        
        self.gen = generator
        self.seed = generator.seed

        self.tiles = generator.tiles

        self.s = SimpleNamespace(**generator.settings[self.__class__.__name__])

    def get(self, x, y, z, tile):

        return tile

    def get_at(self, x, y, z, tile=0):

        return self.get(x, y, z, tile)
