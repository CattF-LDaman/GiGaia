from .entity import Entity
from .physical import Physical

from GiGaia.GiCore.Data.datatypes import D_RBG, D_INT128

import random

class Doomfly(Physical):

    ID = 666
    NAME = "Doomfly"

    PROPERTIES = {
        ("color", D_RBG): (255,0,0),
        ("resting", D_INT128): 0,
    }


    def __init__(self, eid, position=(0,0)):
        super().__init__(eid, position)
