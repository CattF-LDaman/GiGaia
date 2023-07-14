
from GiGaia.GiCore.random_util import seeded_randchoice
from GiGaia.GiCore.Game.World import TILE_SPRITE_SIZE
from GiGaia.GiCore.sprite_util import rotate, replace_color

import pygame
import os

def load(man):
    man.instance.log("[ASSETS] Loading items...")

    data = man.assets["data"]

    for item in data.Items.__dict__.values():
        item["sprite"] = pygame.transform.scale(pygame.image.load(os.path.join(man.location, "Items", item["sprite"]+".png")), (18,18))

    
