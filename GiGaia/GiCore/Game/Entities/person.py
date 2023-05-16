
from .entity import Entity
from .physical import Physical

from GiGaia.GiCore.Data.datatypes import D_BOOL, D_STRING, D_INT16, D_INT32, D_DEC

class Person(Physical):

    ID = 1
    NAME = "Person"

    PROPERTIES = {
        ("has_bacon", D_BOOL): False,
        ("speed", D_INT16): 3000,
        ("jump_strength", D_INT16): 650,
        ("flying", D_BOOL): False,
        ("flight_speed", D_INT32): 5000,
    }


    def __init__(self, eid, position=(0,0)):
        super().__init__(eid, position)
