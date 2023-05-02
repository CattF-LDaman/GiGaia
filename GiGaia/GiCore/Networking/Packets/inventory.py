
from GiGaia.GiCore.Data.datatypes import D_STRING, D_INT16, D_DDICT

SC_ADD_ITEM = (
    ("container", D_STRING, 1),
    ("item_id",D_STRING,1),
    ("amount",D_INT16),
    ("data", D_DDICT, 8)
)

SC_ADD_CONTAINER = (
    ("container" ,D_STRING, 1),
)