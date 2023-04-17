from .Layers import SETTINGS as DEFAULT_SETTINGS
from .Layers import LAYERS

class Generator:

    def __init__(self, seed, tiles, settings={}):  # default arg is allowed to be mutable here bitch
        
        self.seed = seed
        self.settings = self.s = {**DEFAULT_SETTINGS, **settings}

        self.tiles = tiles  # AssetsManager.TIDS (SimpleNamespace)

        self.layers = [layer(self) for layer in LAYERS]

    def get_at(self, x, y, z):

        tile = 0
        for l in self.layers:

            tile = l.get_at(x, y, z, tile)

        return tile