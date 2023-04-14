
from .entity import Entity

from GiGaia.GiCore.Data.datatypes import D_BOOL, D_STRING

class Person(Entity):

    ID = 1
    NAME = "Person"

    PROPERTIES = {
        ("has_bacon", D_BOOL): False,
        ("name", D_STRING, 1): "Paul"
    }


    def __init__(self, eid, position=(0,0)):
        super().__init__(eid, position)
