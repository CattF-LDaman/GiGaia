
from GiGaia.GiCore.Data.datatypes import D_INT64, D_DATA, D_POS

SC_ENTITY = (
    ("eid", D_INT64),
    ("position", D_POS),
    ("props", D_DATA, 4)
)

SC_ENTITY_POS = (
    ("eid", D_INT64),
    ("position", D_POS),
)

SC_ENTITY_UPD_PROP = (
    ("eid", D_INT64),
    ("props", D_DATA, 4)
)