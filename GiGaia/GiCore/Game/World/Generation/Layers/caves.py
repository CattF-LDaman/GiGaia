from .layer import Layer

import math
import opensimplex

class Caves(Layer):

    SETTINGS = {
        "cave_threshold": 0.09,
        "cave_smooth": 30,
        "cave_height_fallof": 20000
    }

    def __init__(self, generator):
        super().__init__(generator)

        self.noise = opensimplex.OpenSimplex(seed=self.gen.seed//23+1337)

        self.threshold = self.s.cave_threshold
        self.smooth_mult = 1/self.s.cave_smooth

        self.cfallof = 1/self.s.cave_height_fallof
        
    def _caved_at(self, x, y):
        thr = min(self.threshold + (y*self.cfallof), self.threshold)
        nval = self.noise.noise2(x*self.smooth_mult, y*self.smooth_mult)

        return nval < thr and nval > -thr

    def get(self, x, y, z, tile):

        if z == 1:
            return tile
        
        if self._caved_at(x, y):
            return 0
        
        return tile