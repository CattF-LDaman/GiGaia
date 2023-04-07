from GiGaia.GiCore.Data.datatypes import D_INT8, D_INT16, D_STRING, D_BOOL, D_RAW


SC_LOAD_STATE = (
    ("sid",D_INT8),
)

SC_GAME_INFO = (
    ("name", D_STRING, 1),
    ("description", D_STRING, 2),
    ("connected", D_INT16),
    ("user_exist",D_BOOL)
)

CS_LOGIN = (
    ("user", D_STRING, 1),
    ("password", D_RAW, 1)
)

SC_LOGIN_CONFIRM = (
    ("is_ok", D_BOOL),
    ("msg", D_STRING, 1)
)