from .entity import Entity
from .physical import Physical

from GiGaia.GiCore.Data.datatypes import D_RBG

import random

class Bitch(Physical):

    ID = 3
    NAME = "Bitch"

    PROPERTIES = {
        ("color", D_RBG): (255,0,0),
    }


    def __init__(self, eid, position=(0,0)):
        super().__init__(eid, position)
