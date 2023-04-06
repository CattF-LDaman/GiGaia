
from types import SimpleNamespace

from POA.POACore.Data.datatypes import pack, unpack, DATATYPES, DT_SIZE, D_INT8, D_INT16

from .general import SC_TEST
from .game import SC_LOAD_STATE, SC_GAME_INFO, CS_CREATE_NATION, SC_NATION_OK

PACKET_TYPES = {
0: SC_TEST,

10: SC_LOAD_STATE,
11: SC_GAME_INFO,

20: CS_CREATE_NATION,
21: SC_NATION_OK,

}

PACKET_NAMES = {
0: "SC_TEST",

10: "SC_LOAD_STATE",
11: "SC_GAME_INFO",

20: "CS_CREATE_NATION",
21: "SC_NATION_OK"
}

PACKET_NAMETYPES = {value:key for key,value in PACKET_NAMES.items()}
PID = SimpleNamespace(**PACKET_NAMETYPES)

_FIELD_NAME = 0
_FIELD_DATATYPE = 1
_FIELD_DATATYPE_LENSIZE = 2 # only for varied-size datatypes eg. D_STRING

def create_packet(packet_type,packet_data):

    packet_data_packed = b""
    for field in PACKET_TYPES[packet_type]:

        field_data = packet_data[field[_FIELD_NAME]]
        field_data_packed = pack(field[_FIELD_DATATYPE], field_data)

        if DATATYPES[field[_FIELD_DATATYPE]][DT_SIZE] is None:

            field_len = len(field_data_packed)
            field_len_packed = field_len.to_bytes(field[_FIELD_DATATYPE_LENSIZE], "little")
            field_packed = field_len_packed + field_data_packed

        else:

            field_packed = field_data_packed

        packet_data_packed += field_packed

    packet_packed = pack(D_INT8, packet_type)+packet_data_packed

    return packet_packed

def read_packet(packet_data):

    packet_type = packet_data[0]

    if packet_type not in PACKET_TYPES:

        raise ValueError("unknown packet type")

    packet_out = {}

    cur_index = 1
    for field in PACKET_TYPES[packet_type]:

        if DATATYPES[field[_FIELD_DATATYPE]][DT_SIZE] is None:

            field_len = int.from_bytes(packet_data[cur_index:cur_index+field[_FIELD_DATATYPE_LENSIZE]], "little")
            cur_index+=field[_FIELD_DATATYPE_LENSIZE]

        else:

            field_len = DATATYPES[field[_FIELD_DATATYPE]][DT_SIZE]

        field_data_packed = packet_data[cur_index:cur_index+field_len]
        field_data = unpack(field[_FIELD_DATATYPE],field_data_packed)

        packet_out[field[_FIELD_NAME]] = field_data

        cur_index += field_len

    packet_out["_PNAME"] = PACKET_NAMES[packet_type]

    return packet_type, SimpleNamespace(**packet_out)
