
from GiGaia.GiCore.Data.datafile import Datafile
from GiGaia.GiCore.Data.datatypes import D_INT16

import os
import pygame

class Keybinds(Datafile):

    DEFAULT_KEYBINDS = {
        "MOVE_UP": pygame.K_z,
        "MOVE_DOWN": pygame.K_s,
        "MOVE_LEFT": pygame.K_q,
        "MOVE_RIGHT": pygame.K_d
    }

    AUTO_CREATE = True

    DATA_VERSION = 1
    STRUC = [
        (keyb, D_INT16) for keyb in DEFAULT_KEYBINDS.keys() 
    ]

    def __init__(self, client_location):
        super().__init__(os.path.join(client_location, "keybinds"))

    def on_create(self):
        
        for k,v in self.DEFAULT_KEYBINDS.items():
            setattr(self, k, v)

    