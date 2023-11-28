
import pygame
from functools import lru_cache

@lru_cache(maxsize=1024*6)
def create_colorized_radial_gradient(radius, center_color, outer_color, intensity=1):
    size = (2 * radius, 2 * radius)
    surface = pygame.Surface(size)#, pygame.SRCALPHA)
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
            #alpha = abs(int(center_color[3] + normalized_distance * (outer_color[3] - center_color[3])))

            pixels[x, y] = pygame.Color(*interpolated_color)#, alpha)
    
    del pixels
    for _ in range(intensity-1):
        surface.blit(surface.copy(), (0,0), special_flags=pygame.BLEND_ADD)
    return surface

class LuxFlux:

    WORLD_LIGHT_LEVELS = 10

    def __init__(self, state):

        self.state = state
        self.game = state.game

        self.resize()

        for c in range(20):
            self.preload_point_light(self.state.world.dev_light_radius, self.state.world.dev_light_color(c), self.state.world.dev_light_intensity)

    def preload_point_light(self, radius, color=(255,255,255), intensity=1):
        create_colorized_radial_gradient(radius, color, (0,0,0), intensity)

    def point_light(self, location, radius, color=(255,255,255), intensity=1):

        gr = create_colorized_radial_gradient(radius, color, (0,0,0), intensity)
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
        light = min(sum(self.state.world.sky_color)/3*1.5,255)
        return (light,) * 3  

    def resize(self):

        self.light_surface = pygame.Surface(self.game.size)        
        self.lit_up_surface = pygame.Surface(self.game.size)
        self.lit_up_surface.set_colorkey((0,0,0))
        self.reset()

    def reset(self):
        self.light_surface.fill(self.natural_light)
        self.lit_up_surface.fill(((0,0,0)))

    def apply(self):

        self.game.screen.blit(self.light_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.game.screen.blit(self.lit_up_surface, (0, 0))
        
        self.reset()
