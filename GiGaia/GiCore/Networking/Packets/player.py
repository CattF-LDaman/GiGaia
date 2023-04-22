
from GiGaia.GiCore.Data.datatypes import D_INT16S, D_FPOS, D_TILEREF, D_INT16

CS_MOVE = (
    ("x", D_INT16S),
    ("y", D_INT16S)
)

CS_WSET = (
    ("chunk", D_FPOS),
    ("tileref", D_TILEREF),
    ("tile", D_INT16)
)