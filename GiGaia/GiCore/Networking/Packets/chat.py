
from GiGaia.GiCore.Data.datatypes import D_STRING

# Send a chat
CS_CHAT_OUT = (
    ('content', D_STRING, 2),
)

# Recv a chat
SC_CHAT = (
    ('user', D_STRING, 1),
    ('content', D_STRING, 2)
)
