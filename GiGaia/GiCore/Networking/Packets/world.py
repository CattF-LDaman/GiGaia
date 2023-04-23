
from GiGaia.GiCore.Data.datatypes import D_CHUNK, D_FPOS, D_TILEREF, D_INT16, D_DEC

# Make chunk known to client
SC_CHUNK = (
    ("position", D_FPOS),
    ("tiles",D_CHUNK)
)

# Change a tile of a chunk on the client
SC_UPDATE_TILE = (
    ("chunk", D_FPOS),
    ("tileref", D_TILEREF),
    ("tile", D_INT16)
)

# Update the entire chunk on client
SC_UPDATE_CHUNK = (
    ("chunk", D_FPOS),
    ("tiles", D_CHUNK)
)

SC_TIME = (
    ("time", D_DEC),
)