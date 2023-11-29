from .layer import Layer
from GiGaia.GiCore.random_util import seeded_randint

import math
import opensimplex

class TreeTest(Layer):

    SETTINGS = {
        "treetest_chance": 0.14,
        "treetest_len": 16
    }

    def __init__(self, generator):
        super().__init__(generator)

        self.treeseed = self.gen.seed//17+17746
    
        self.chance = self.s.treetest_chance*100
        self.length = self.s.treetest_len
        
    def _tree_at(self, x, y):

        if not self.gen.layers[0].is_ground(x, y+self.length):
            return False
        
        return seeded_randint(0, 100, x+self.treeseed) <= self.chance

    def get(self, x, y, z, tile):

        if tile != 0 or y > 0 or z == 0 or x % 2 != 0:
            return tile
        
        if self._tree_at(x, y):
            return self.tiles.WOODPLATFORM
    
        return tile
    
