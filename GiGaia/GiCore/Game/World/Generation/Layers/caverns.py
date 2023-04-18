from .layer import Layer

import opensimplex

class Caverns(Layer):

    SETTINGS = {
        "cavern_threshold": 0.45,
        "cavern_smooth": 60
    }

    def __init__(self, generator):
        super().__init__(generator)

        self.noise = opensimplex.OpenSimplex(seed=self.gen.seed//20+1347)

        self.threshold = self.s.cavern_threshold
        self.smooth_mult = 1/self.s.cavern_smooth
        
    def _caved_at(self, x, y):
        
        nval = self.noise.noise2(x*self.smooth_mult, y*self.smooth_mult)

        return nval > max(self.threshold*(-y/80), self.threshold)

    def get(self, x, y, z, tile):

        if z == 1:
            return tile
        
        if self._caved_at(x, y):
            return 0
        
        return tile