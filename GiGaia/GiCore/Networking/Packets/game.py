from GiGaia.GiCore.Data.datatypes import D_INT8, D_INT16, D_STRING, D_BOOL, D_RAW, D_RBG


SC_LOAD_STATE = (
    ("sid",D_INT8),
)

A_WAITING = ()

SC_GAME_INFO = (
    ("name", D_STRING, 1),
    ("theme_color", D_RBG),
    ("description", D_STRING, 2),
    ("connected", D_INT16),
    ("user_exist",D_BOOL)
)

CS_LOGIN = (
    ("password", D_RAW, 1),
)

SC_LOGIN_CONFIRM = (
    ("is_ok", D_BOOL),
    ("msg", D_STRING, 1)
)