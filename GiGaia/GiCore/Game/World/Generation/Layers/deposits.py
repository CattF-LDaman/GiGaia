from .layer import Layer
from GiGaia.GiCore.random_util import seeded_randchoice

import math
import opensimplex

class LimestoneDeposits(Layer):

    SETTINGS = {
        "limestdep_threshold": 0.6,
        "limestdep_smooth": 20
    }

    def __init__(self, generator):
        super().__init__(generator)

        self.noise = opensimplex.OpenSimplex(seed=self.gen.seed//23+1647)
        self.noisez = opensimplex.OpenSimplex(seed=self.gen.seed//27+127)

        self.threshold = self.s.limestdep_threshold
        self.smooth_mult = 1/self.s.limestdep_smooth
        
    def _st_at(self, x, y, z):
        
        nval = (self.noise if z else self.noisez).noise2(x*self.smooth_mult, y*self.smooth_mult)

        return nval > self.threshold

    def get(self, x, y, z, tile):

        if tile == self.tiles.STONE:
            if self._st_at(x, y, z):
                return self.tiles.LIMESTONE
        
        return tile
    
class GraniteDeposits(Layer):

    SETTINGS = {
        "grandep_threshold": 0.61,
        "grandep_smooth": 16
    }

    def __init__(self, generator):
        super().__init__(generator)

        self.noise = opensimplex.OpenSimplex(seed=self.gen.seed//22+1048)
        self.noisez = opensimplex.OpenSimplex(seed=self.gen.seed//24+161)

        self.threshold = self.s.grandep_threshold
        self.smooth_mult = 1/self.s.grandep_smooth
        
    def _st_at(self, x, y, z):
        
        nval = (self.noise if z else self.noisez).noise2(x*self.smooth_mult, y*self.smooth_mult)

        return nval > self.threshold

    def get(self, x, y, z, tile):

        if tile == self.tiles.STONE:
            if self._st_at(x, y, z):
                return self.tiles.GRANITE
        
        return tile

class CoalDeposits(Layer):

    SETTINGS = {
        "stcoaldep_threshold": 0.65,
        "stcoaldep_thresholdz": 0.67,
        "stcoaldep_smooth": 8
    }

    def __init__(self, generator):
        super().__init__(generator)

        self.noise = opensimplex.OpenSimplex(seed=self.gen.seed//17+1018)

        self.threshold = self.s.stcoaldep_threshold
        self.thresholdz = self.s.stcoaldep_thresholdz
        self.smooth_mult = 1/self.s.stcoaldep_smooth
        
    def _st_at(self, x, y, z):
        
        nval = self.noise.noise2(x*self.smooth_mult, y*self.smooth_mult)

        return nval > (self.threshold if z == 0 else self.thresholdz)

    def get(self, x, y, z, tile):

        if tile == self.tiles.STONE:
            if self._st_at(x, y, z):
                return self.tiles.STONECOAL
        
        return tile