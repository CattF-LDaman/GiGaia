
from GiGaia.GiCore.Data.datafile import Datafile
from GiGaia.GiCore.Data.datatypes import D_INT32

import os
import pygame

class Keybinds(Datafile):

    DEFAULT_KEYBINDS = {
        "MOVE_DOWN": pygame.K_s,
        "MOVE_LEFT": pygame.K_q,
        "MOVE_RIGHT": pygame.K_d,
        "JUMP": pygame.K_SPACE,
        "CROUCH": pygame.K_LSHIFT,
        "INVENTORY": pygame.K_i,
        "CHAT": pygame.K_t,
        "CHAT_SEND": pygame.K_RETURN,
        "CHAT_HUP": pygame.K_UP,
        "CHAT_HDOWN": pygame.K_DOWN,
        "FREELOOK": pygame.K_LALT,
        "STRUCTURIZER": pygame.K_F1
    }

    AUTO_CREATE = True

    DATA_VERSION = 5
    STRUC = [
        (keyb, D_INT32) for keyb in DEFAULT_KEYBINDS.keys() 
    ]

    def __init__(self, client_location):
        super().__init__(os.path.join(client_location, "keybinds"))

    def on_create(self):
        
        for k,v in self.DEFAULT_KEYBINDS.items():
            setattr(self, k, v)

    