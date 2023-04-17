
from GiGaia.GiCore.Game.World.Generation import Generator
from GiGaia.GiCore.Game.World import CHUNK_SIZE_TILES, REGION_SIZE_TILES

from types import SimpleNamespace
import pygame
pygame.init()

screen = pygame.display.set_mode((1000,1000))
pixa = pygame.PixelArray(screen)

seed = 3456789

tiles = SimpleNamespace(**{"DIRT": 1, "STONE": 2})

gen = Generator(seed, tiles)

tc = {0:(0, 0, 0), 1:(153, 102, 51), 2:(115, 115, 115)}
tdc = {0:(0, 0, 0), 1:(153//2, 102//2, 51//2), 2:(115//2, 115//2, 115//2)}


for x in range(1000):
    for y in range(1000):
        sy = y
        sx = x
        y = y - 500

        if y == 0:
            pixa[x,sy] = (255,0,0)
        elif y % REGION_SIZE_TILES == 0:
            pixa[x,sy] = (0,255,0)
        elif x % REGION_SIZE_TILES == 0:
            pixa[x,sy] = (0,255,0)
        elif y % CHUNK_SIZE_TILES == 0:
            pixa[x,sy] = (0,0,255)
        elif x % CHUNK_SIZE_TILES == 0:
            pixa[x,sy] = (0,0,255)
        else:
            c = tc[gen.get_at(x,y,0)]
            if not c:
                c = tdc[gen.get_at(x,y,1)]

            pixa[x,sy] = c

    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()

while True:

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()

    pygame.display.flip()