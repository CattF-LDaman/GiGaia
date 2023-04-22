
from types import SimpleNamespace

from GiGaia.GiCore.Data.datatypes import pack, unpack, DATATYPES, DT_SIZE

_FIELD_NAME = 0
_FIELD_DATATYPE = 1
_FIELD_DATATYPE_LENSIZE = 2 # only for varied-size datatypes eg. D_STRING

def build_struc(struc,struc_data):
    
    struc_packed = b""
    for field in struc:

        field_data = struc_data[field[_FIELD_NAME]]
        field_data_packed = pack(field[_FIELD_DATATYPE], field_data)

        if DATATYPES[field[_FIELD_DATATYPE]][DT_SIZE] is None:

            field_len = len(field_data_packed)
            field_len_packed = field_len.to_bytes(field[_FIELD_DATATYPE_LENSIZE], "little")
            field_packed = field_len_packed + field_data_packed

        else:

            field_packed = field_data_packed

        struc_packed += field_packed

    return struc_packed

def read_struc(struc, struc_data, namespace=True):

    packet_out = {}

    cur_index = 0
    for field in struc:

        if DATATYPES[field[_FIELD_DATATYPE]][DT_SIZE] is None:

            field_len = int.from_bytes(struc_data[cur_index:cur_index+field[_FIELD_DATATYPE_LENSIZE]], "little")
            cur_index+=field[_FIELD_DATATYPE_LENSIZE]

        else:

            field_len = DATATYPES[field[_FIELD_DATATYPE]][DT_SIZE]

        field_data_packed = struc_data[cur_index:cur_index+field_len]
        field_data = unpack(field[_FIELD_DATATYPE],field_data_packed)

        packet_out[field[_FIELD_NAME]] = field_data

        cur_index += field_len

    return SimpleNamespace(**packet_out) if namespace else packet_out
