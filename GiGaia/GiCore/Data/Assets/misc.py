
import pygame
import os

def load(man):
    man.instance.log("[ASSETS] Loading misc...")

    man.assets['window'] = pygame.image.load(os.path.join(man.location, "window.png"))