
from GiGaia.GiCore.Data.datatypes import D_INT8S, D_FPOS, D_TILEREF, D_INT16

CS_MOVE = (
    ("x", D_INT8S),
)

CS_JUMP = ()

CS_WSET = (
    ("chunk", D_FPOS),
    ("tileref", D_TILEREF),
    ("tile", D_INT16)
)

CS_CROUCH = ()