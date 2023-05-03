
from types import SimpleNamespace

from GiGaia.GiCore.Data.datatypes import pack, D_INT8
from GiGaia.GiCore.Data import struc

from .general import SC_TEST
from .game import SC_LOAD_STATE, SC_GAME_INFO, CS_LOGIN, SC_LOGIN_CONFIRM, A_WAITING, SC_PLAYER
from .entity import SC_ENTITY, SC_ENTITY_POS, SC_ENTITY_UPD_PROP, SC_ENTITY_DESTROY
from .player import CS_MOVE, CS_WSET, CS_JUMP, CS_CROUCH
from .world import SC_CHUNK, SC_UPDATE_CHUNK, SC_UPDATE_TILE, SC_TIME
from .inventory import SC_ADD_ITEM, SC_ADD_CONTAINER
from .chat import SC_CHAT, CS_CHAT_OUT

PACKET_TYPES = {
0: SC_TEST,
1: SC_CHAT,
2: CS_CHAT_OUT,

10: SC_LOAD_STATE,
11: SC_GAME_INFO,
12: A_WAITING,

13: SC_PLAYER,

20: CS_LOGIN,
21: SC_LOGIN_CONFIRM,

40: SC_ENTITY,
41: SC_ENTITY_POS,
42: SC_ENTITY_UPD_PROP,
43: SC_ENTITY_DESTROY,

50: CS_MOVE,
51: CS_WSET,
52: CS_JUMP,
53: CS_CROUCH,

60: SC_CHUNK,
61: SC_UPDATE_CHUNK,
62: SC_UPDATE_TILE,
63: SC_TIME,

70: SC_ADD_ITEM,
71: SC_ADD_CONTAINER,

}

PACKET_NAMES = {
0: "SC_TEST",
1: "SC_CHAT",
2: "CS_CHAT_OUT",

10: "SC_LOAD_STATE",
11: "SC_GAME_INFO",
12: "A_WAITING",

13: "SC_PLAYER",

20: "CS_LOGIN",
21: "SC_LOGIN_CONFIRM",

40: "SC_ENTITY",
41: "SC_ENTITY_POS",
42: "SC_ENTITY_UPD_PROP",
43: "SC_ENTITY_DESTROY",

50: "CS_MOVE",
51: "CS_WSET",
52: "CS_JUMP",
53: "CS_CROUCH",

60: "SC_CHUNK",
61: "SC_UPDATE_CHUNK",
62: "SC_UPDATE_TILE",
63: "SC_TIME",

70: "SC_ADD_ITEM",
71: "SC_ADD_CONTAINER",

}

PACKET_NAMETYPES = {value:key for key,value in PACKET_NAMES.items()}
PID = SimpleNamespace(**PACKET_NAMETYPES)

def create_packet(packet_type, packet_data):

    packet_data_packed = struc.build_struc(PACKET_TYPES[packet_type], packet_data)
    packet_data = pack(D_INT8, packet_type)+packet_data_packed

    return packet_data

def read_packet(packet_data):

    packet_type = packet_data[0]
    packet_data = packet_data[1:]

    if packet_type not in PACKET_TYPES:
        raise ValueError("unknown packet type")
    
    packet_out = struc.read_struc(PACKET_TYPES[packet_type], packet_data).__dict__
    packet_out['_PNAME'] = PACKET_NAMES[packet_type]

    return packet_type, SimpleNamespace(**packet_out)
