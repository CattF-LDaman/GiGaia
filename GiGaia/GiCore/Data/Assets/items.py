
from types import SimpleNamespace

import pygame
import os

def load(man):
    man.instance.log("[ASSETS] Loading items...")

    data = man.assets["data"]

    for item in data.Items.__dict__.values():
        if type(item["sprite"]) == str:
            item["sprite"] = pygame.image.load(os.path.join(man.location, "Items", item["sprite"]+".png"))

    man.items = {item_name:SimpleNamespace(**item) for item_name, item in data.Items.__dict__.items()}
