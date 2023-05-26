from GiGaia.GiCore.Data.datatypes import D_INT8, D_INT16, D_INT64, D_STRING, D_BOOL, D_RAW, D_RBG

# Makes client switch game state
SC_LOAD_STATE = (
    ("sid",D_INT8),
)

# An empty packet
A_WAITING = ()

# Information for user when joining
SC_GAME_INFO = (
    ("name", D_STRING, 1),
    ("theme_color", D_RBG),
    ("description", D_STRING, 2),
    ("connected", D_INT16),
    ("user_exist",D_BOOL),
    ("tickrate",D_INT16)
)

# Login packet, 'password' is actually a hash
CS_LOGIN = (
    ("password", D_RAW, 1),
)

# Sent to client to know if login credentials were correct 
SC_LOGIN_CONFIRM = (
    ("is_ok", D_BOOL),
    ("msg", D_STRING, 1)
)

# Makes player EID known to client
SC_PLAYER = (
    ("eid", D_INT64),
)

SC_BYE = (
    ("reason", D_STRING, 2),
)