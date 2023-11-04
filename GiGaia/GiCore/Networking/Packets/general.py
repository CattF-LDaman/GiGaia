
from GiGaia.GiCore.Data.datatypes import D_INT64, D_INT16, D_STRING

A_PING = (
    ("timestamp",D_INT64),
)

SC_REPORT_PING = (
    ("ms", D_INT16),
)

SC_SOUND = (
    ("sound", D_STRING, 1),
)

A_THROUGHPUT = (
    ("tpstart", D_INT64),
    ("n", D_INT64),
    ("nmax", D_INT64)
)

A_THROUGHPUT_FINISH = (
    ("tpstart", D_INT64),
)