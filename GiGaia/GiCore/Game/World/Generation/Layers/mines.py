from .layer import Layer
from GiGaia.GiCore.random_util import seeded_randint

import math
import opensimplex

class Mine(Layer):

    SETTINGS = {
        "mine_chance_per_space": 0.3,
        "mine_space_width": 600,
    }

    def __init__(self, generator):
        super().__init__(generator)

        self.mineseed = self.gen.seed//13+45678
    
        self.chance = self.s.mine_chance_per_space*100
        self.space_width = self.s.mine_space_width
        
        self.structure = self.structures.MINE

    def _has_mine(self, space):
        
        return seeded_randint(0, 100, self.mineseed+hash(space)+3667) <= self.chance

    def _mine_location(self, space):
        return seeded_randint(space*self.space_width+self.structure.width, space*self.space_width+self.space_width-1-self.structure.width, space*self.mineseed)

    def _mine_core(self, space):
        x = self._mine_location(space)
        y = -self.gen.layers[0].height_at(x)
        return self._mine_location(space), y

    def _space(self, x):
        return int(x/self.space_width) 

    def get(self, x, y, z, tile):

        space = self._space(x)

        if y > 0 or not self._has_mine(space):
            return tile
        
        mine_wcore = self._mine_core(space)

        if not self.structure.within((x,y), mine_wcore): # THIS BITCH DOESN'T WANT TO WORK BELOW X 0
            return tile
        
        struc_tile = self.structure.get_at(x, y, z, mine_wcore)
        if struc_tile == self.tiles.STRUCFILL:
            return tile
        return struc_tile if struc_tile is not None else tile
