
from .entity import Entity

from GiGaia.GiCore.Data.datatypes import D_INT16, D_VEC2, D_DEC, D_BOOL

class Physical(Entity):

    ID = 3
    NAME = "Physical"

    PROPERTIES = {
        #("vel", D_VEC2): (0,0),
        ("mass", D_DEC): 1,
        ("friction", D_DEC): 2,
        ("air_friction", D_DEC): 1,
        ("width", D_INT16): 1,
        ("height", D_INT16): 1,
        ("has_gravity", D_BOOL): True,
        ("noclip", D_BOOL): False,
    }


    def __init__(self, eid, position=(0,0)):
        super().__init__(eid, position)
