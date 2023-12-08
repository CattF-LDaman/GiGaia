from .layer import Layer
from GiGaia.GiCore.random_util import seeded_randint

import math
import opensimplex

class House(Layer):

    SETTINGS = {
        "house_chance_per_space": 0.2,
        "house_space_width": 1000,
    }

    def __init__(self, generator):
        super().__init__(generator)

        self.houseseed = self.gen.seed//19+18748
    
        self.chance = self.s.house_chance_per_space*100
        self.space_width = self.s.house_space_width
        
        self.structure = self.structures.HOUSE

    def _has_house(self, space):
        
        return seeded_randint(0, 100, self.houseseed+hash(space)+1234) <= self.chance

    def _house_location(self, space):
        return seeded_randint(space*self.space_width+self.structure.width, space*self.space_width+self.space_width-1-self.structure.width, space*self.houseseed)

    def _house_core(self, space):
        x = self._house_location(space)
        y = -self.gen.layers[0].height_at(x)
        return self._house_location(space), y

    def _space(self, x):
        return int(x/self.space_width) 

    def get(self, x, y, z, tile):

        space = self._space(x)

        if y > 0 or not self._has_house(space):
            return tile
        
        house_wcore = self._house_core(space)

        if not self.structure.within((x,y), house_wcore):
            return tile
        
        struc_tile = self.structure.get_at(x, y, z, house_wcore)
        if struc_tile == self.tiles.STRUCFILL:
            return tile
        return struc_tile if struc_tile is not None else tile
