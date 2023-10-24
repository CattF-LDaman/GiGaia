
from . import datafiles, fonts, sounds, tiles, items, misc

import traceback
import os
import pygame
import pathlib
import json
import types

class AssetsManager:

    def __init__(self, instance):

        self.instance = instance
        self.location = instance.dirs["assets"]

        self.assets = {"fonts":{}, "icon":None, "data":{}, "sounds":{}, "window":None}

    def __getitem__(self, indx):
        return self.assets.get(indx)

    def load(self):

        datafiles.load(self)
        fonts.load(self)
        sounds.load(self)
        tiles.load(self)
        items.load(self)
        misc.load(self)

        self.load_icon()

        for category, data in self.assets.items():
            setattr(self, category, data)

        self.assets = types.SimpleNamespace(**self.assets)
        self.instance.log("[ASSETS] Done loading assets.")


    def load_icon(self):

        self.instance.log("[ASSETS] Loading icon...")
        self.assets['icon'] = pygame.transform.scale(pygame.image.load(os.path.join(self.location,'icon.png')),(64,64))
