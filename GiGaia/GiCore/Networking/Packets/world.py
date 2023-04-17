
from GiGaia.GiCore.Data.datatypes import D_CHUNK, D_POS, D_TILEREF, D_INT16

SC_CHUNK = (
    ("position", D_POS),
    ("tiles",D_CHUNK)
)

SC_UPDATE_TILE = (
    ("chunk", D_POS),
    ("tileref", D_TILEREF),
    ("tile", D_INT16)
)

SC_UPDATE_CHUNK = (
    ("chunk", D_POS),
    ("tiles", D_CHUNK)
)