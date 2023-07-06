
from GiGaia.GiCore.Game.World.Generation import Generator
from GiGaia.GiCore.Game.World import CHUNK_SIZE_TILES, REGION_SIZE_TILES

from types import SimpleNamespace
import multiprocessing

import pygame
pygame.init()

screen = pygame.Surface((10000, 5000))
pixa = pygame.PixelArray(screen)

seed = 3456789

tiles = SimpleNamespace(**{"DIRT": 1, "STONE": 2, "CUM":3, "GRASS":5, "PLATFORM":3, "PIPE":4})

gen = Generator(seed, tiles)

tc = {0:(0, 0, 0), 1:(153, 102, 51), 2:(115, 115, 115), 5:(117, 56, 27)}
tdc = {0:(0, 0, 0), 1:(153//2, 102//2, 51//2), 2:(115//2, 115//2, 115//2), 5:(117//2, 56//2, 27//2)}


for x in range(10000):
    for y in range(5000):
        sy = y
        sx = x
        y = y - 500


        c = tc[gen.get_at(x,y,0)]
        if not c:
            c = tdc[gen.get_at(x,y,1)]

        pixa[x,sy] = c

    print(x/10000*100)

pygame.image.save(screen, "gentest.png")