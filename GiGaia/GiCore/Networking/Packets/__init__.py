
from types import SimpleNamespace

from GiGaia.GiCore.Data.datatypes import pack, D_INT8
from GiGaia.GiCore.Data import struc

from .general import SC_TEST
from .game import SC_LOAD_STATE, SC_GAME_INFO, CS_LOGIN, SC_LOGIN_CONFIRM, A_WAITING

PACKET_TYPES = {
0: SC_TEST,

10: SC_LOAD_STATE,
11: SC_GAME_INFO,
12: A_WAITING,

20: CS_LOGIN,
21: SC_LOGIN_CONFIRM,

69: SC_KSTR

}

PACKET_NAMES = {
0: "SC_TEST",

10: "SC_LOAD_STATE",
11: "SC_GAME_INFO",
12: "A_WAITING",

20: "CS_LOGIN",
21: "SC_LOGIN_CONFIRM",

69:"SC_KSTR"

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
