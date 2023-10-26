
import pygame
import os

def load(man):
    man.instance.log("[ASSETS] Loading misc...")

    man.assets['window'] = pygame.image.load(os.path.join(man.location, "window.png"))
    man.assets['background'] = pygame.image.load(os.path.join(man.location, "background.png"))
    man.assets['page_background'] = pygame.image.load(os.path.join(man.location, "inner_background2.png"))