
from .entity import Entity
from .physical import Physical

from GiGaia.GiCore.Data.datatypes import D_INT64, D_STRING

class ItemEntity(Physical):

    ID = 111
    NAME = "ItemEntity"

    PROPERTIES = {
        ("amount", D_INT64): 1,
        ("item", D_STRING, 1): "jonko",
    }


    def __init__(self, eid, position=(0,0)):
        super().__init__(eid, position)
