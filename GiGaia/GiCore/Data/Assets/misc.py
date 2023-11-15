
import pygame
import os

def load(man):
    man.instance.log("[ASSETS] Loading misc...")

    man.assets['background'] = pygame.image.load(os.path.join(man.location, "background.png"))
    man.assets['page_background'] = pygame.image.load(os.path.join(man.location, "inner_background2.png"))
    man.assets['window'] = pygame.transform.scale2x(pygame.image.load(os.path.join(man.location, "inner_background2.png")))
