
from .entity import Entity

from GiGaia.GiCore.Data.datatypes import D_INT64

class Bob(Entity):

    ID = 2
    NAME = "Bob"

    PROPERTIES = {
        ("coins", D_INT64): 0,
    }


    def __init__(self, eid, position=(0,0)):
        super().__init__(eid, position)
