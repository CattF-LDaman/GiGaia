
import json

def pack_bool(data):

    return b'\x01' if data else b'\x00'

def unpack_bool(data):

    return bool(data[0])

def pack_int(data, intsize):

    return data.to_bytes(intsize,"little")

def unpack_int(data):

    return int.from_bytes(data, "little")

def pack_int8(data):

    return pack_int(data, 1)

def pack_int16(data):

    return pack_int(data, 2)

def pack_int32(data):

    return pack_int(data, 4)

def pack_int64(data):

    return pack_int(data, 8)

def pack_int_s(data, intsize):

    return data.to_bytes(intsize,"little", signed=True)

def unpack_int_s(data):

    return int.from_bytes(data, "little", signed=True)

def pack_int8_s(data):

    return pack_int_s(data, 1)

def pack_int16_s(data):

    return pack_int_s(data, 2)

def pack_int32_s(data):

    return pack_int_s(data, 4)

def pack_int64_s(data):

    return pack_int_s(data, 8)

def pack_string(data):

    return data.encode('utf-8')

def unpack_string(data):

    return data.decode('utf-8')

def pack_json(data):

    return json.dumps(data).encode('utf-8')

def unpack_json(data):

    return json.loads(data.decode('utf-8'))

def pack_pos(data):

    return pack_int64_s(data[0])+pack_int64_s(data[1])

def unpack_pos(data):

    return [unpack_int_s(data[:8]),unpack_int_s(data[8:])]

def raw(data):

    return data

DT_PACK = 0
DT_UNPACK = 1
DT_SIZE = 2

D_BOOL = 111
D_INT8 = 0
D_INT16 = 1
D_INT32 = 2
D_INT64 = 3
D_INT8S = 4
D_INT16S = 5
D_INT32S = 6
D_INT64S = 7
D_STRING = 8
D_JSON = 9
D_POS = 10
D_RAW = 11

DATATYPES = {

D_BOOL: (pack_bool, unpack_bool, 1),
D_INT8: (pack_int8, unpack_int, 1),
D_INT16: (pack_int16, unpack_int, 2),
D_INT32: (pack_int32, unpack_int, 4),
D_INT64: (pack_int64, unpack_int, 8),
D_INT8S: (pack_int8_s, unpack_int_s, 1),
D_INT16S: (pack_int16_s, unpack_int_s, 2),
D_INT32S: (pack_int32_s, unpack_int_s, 4),
D_INT64S: (pack_int64_s, unpack_int_s, 8),
D_STRING: (pack_string, unpack_string, None), # None marks non-fixed length
D_JSON: (pack_json, unpack_json, None),
D_POS: (pack_pos, unpack_pos, 16),
D_RAW: (raw, raw, None),

}

def unpack(datatype, data):

    return DATATYPES[datatype][DT_UNPACK](data)

def pack(datatype, data):

    return DATATYPES[datatype][DT_PACK](data)
