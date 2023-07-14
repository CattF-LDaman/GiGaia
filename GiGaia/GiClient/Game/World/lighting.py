
import pygame
import multiprocessing
import numpy as np
from functools import lru_cache

@lru_cache(maxsize=512)
def create_colorized_radial_gradient(radius, center_color, outer_color):
    size = (2 * radius, 2 * radius)
    surface = pygame.Surface(size, pygame.SRCALPHA)
    center = (radius, radius)
    pixels = pygame.PixelArray(surface)
    
    for y in range(size[1]):
        for x in range(size[0]):
            pixel = (x, y)
            distance = pygame.math.Vector2(pixel).distance_to(center)
            normalized_distance = max(0, min(distance / radius, 1))
            interpolated_color = (
                abs(int(center_color[0] + normalized_distance * (outer_color[0] - center_color[0]))),
                abs(int(center_color[1] + normalized_distance * (outer_color[1] - center_color[1]))),
                abs(int(center_color[2] + normalized_distance * (outer_color[2] - center_color[2]))),
            )
            alpha = abs(int(center_color[3] + normalized_distance * (outer_color[3] - center_color[3])))

            pixels[x, y] = pygame.Color(*interpolated_color, alpha)
    
    del pixels
    return surface

class LuxFlux:

    WORLD_LIGHT_LEVELS = 10

    def __init__(self, state):

        self.state = state
        self.game = state.game

        self.chunks = LuxChunks(self)

        self.resize()

    def point_light(self, location, radius, color=(255,255,255)):

        gr = create_colorized_radial_gradient(radius, color+ (255,), (0,0,0,255))
        gr_rect = gr.get_rect()
        gr_rect.center = location
        self.light_surface.blit(gr, gr_rect, special_flags=pygame.BLEND_RGB_ADD)

    def free_light_world(self, surf, location):

        screen_loc = self.state.scene.convert_world_to_screen_coord(location)
        self.light_surface.blit(surf, screen_loc)

    def free_light(self, surf, location):

        self.light_surface.blit(surf, location)

    @property
    def natural_light(self):
        light = min(sum(self.state.world.sky_color)/3*2,255)
        return (light,) * 3  

    def resize(self):

        self.light_surface = pygame.Surface(self.game.size)        
        self.light_surface.fill(self.natural_light)

    def apply(self):

        self.game.screen.blit(self.light_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.light_surface.fill(self.natural_light)

class LuxChunks:

    def __init__(self, lux):

        self.lux = lux
        self.game = lux.game
        self.world = lux.state.world

        self.min_chunk = None # topleft most chunk

        self.chunks = []
        self.lighting = []

    def draw_pos(self):

        if not self.min_chunk:
            return (0, 0)
        return self.min_chunk.draw_pos

    def add_chunk(self, c):

        if c in self.chunks:
            return
        
        dp = c.draw_pos
        if not self.min_chunk or dp[0] < self.min_chunk.draw_pos[0] or dp[1] < self.min_chunk.draw_pos[1]:
            self.min_chunk = c

        self.chunks.append(c)

    def smooth_2d_array(self, array):
        rows = len(array)
        cols = len(array[0])
        result = [[0] * cols for _ in range(rows)]
        
        # Convert input array to NumPy array
        array_np = np.array(array)
        
        # Smooth along rows
        smoothed_rows = np.apply_along_axis(lambda x: np.convolve(x, [0.25, 0.5, 0.25], mode='same'), axis=1, arr=array_np)
        
        # Smooth along columns
        smoothed_np = np.apply_along_axis(lambda x: np.convolve(x, [0.25, 0.5, 0.25], mode='same'), axis=0, arr=smoothed_rows.T).T
        
        # Convert smoothed array back to standard Python array
        smoothed = smoothed_np.tolist()
        
        return smoothed

    def update(self):

        for chunk in self.chunks :
            pass


    def draw(self):
        
        self.lux.light_surface.blit()