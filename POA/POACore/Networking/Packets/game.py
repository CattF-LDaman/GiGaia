from POA.POACore.Data.datatypes import D_INT8, D_INT16, D_STRING, D_BOOL


SC_LOAD_STATE = (
                    ("sid",D_INT8),
        )

SC_GAME_INFO = (
    ("name", D_STRING, 1),
    ("description", D_STRING, 2),
    ("connected", D_INT16)
)

CS_CREATE_NATION = (
    ("name", D_STRING, 1),
    ("motto", D_STRING, 1)
)

SC_NATION_OK = (
    ("is_ok", D_BOOL),
    ("msg", D_STRING, 1)
)