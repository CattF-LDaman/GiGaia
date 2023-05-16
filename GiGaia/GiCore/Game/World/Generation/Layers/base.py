from .layer import Layer

import opensimplex
from functools import lru_cache

class Base(Layer):

    SETTINGS = {
        "ground_height": 4000,  # Max height from y=0 to y=-HEIGHT the 'ground' can be
        "ground_base": 3500,

        "crown_base": 8,
        "crown_variance": 4,
        "crown_smooth": 10,
        
        "base_smooth": 11000,  # Gets used in special sauce, lower = more noisey, higher = smoother
        "base_noise_layers": [0.3, 0.2, 0.0, 0.15, 0.3, 0.15],  # weights
        "magic": 3
    }

    def __init__(self, generator):
        super().__init__(generator)

        self.noise = opensimplex.OpenSimplex(seed=self.gen.seed//45+1337)
        self._grab_level = self.gen.seed%1337

        self.layers = len(self.s.base_noise_layers)
        self.weights = self.s.base_noise_layers

        self.ground_height = self.s.ground_height
        self.ground_base = self.s.ground_base
        self.ground_extend = self.ground_height - self.ground_base

        self.crown_base = self.s.crown_base
        self.crown_variance = self.s.crown_variance
        self.crown_smooth_mult = 1/self.s.crown_smooth

        base_smooth = self.s.base_smooth

        self.smooths = [1/(base_smooth/(sl**self.s.magic)) for sl in range(1, self.layers+1)]  # Special Sauce
    
    def normalize(self, n):

        return abs((n+1)/2)

    @lru_cache(None)
    def _height_at(self, x):
        
        nval = sum(self.normalize(self.noise.noise2(x*s, self._grab_level))*w for w,s in zip(self.weights, self.smooths))

        return int(self.crown_base + (self.ground_extend*nval))
    
    def is_crown(self, x, h):

        nval = self.noise.noise2(x*self.crown_smooth_mult, self._grab_level+12345)
        crown = self.crown_base+(nval*self.crown_variance)
        xh = self._height_at(x)

        if h <= -xh+crown:
            return True
        
        return False

    def is_grass(self, x, y):

        return y == -self._height_at(x)

    def is_ground(self, x, y):

        xh = self._height_at(x)
        if y >= -xh:
            return True
        
        return False

    def get(self, x, y, z, tile):

        if not self.is_ground(x,y): 
            return 0
        
        if self.is_crown(x, y):
            if self.is_grass(x, y):
                return self.tiles.GRASS
            return self.tiles.DIRT
            
        return self.tiles.STONE