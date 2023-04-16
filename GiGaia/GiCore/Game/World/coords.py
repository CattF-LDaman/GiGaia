
from . import TILE_SIZE_PIXELS, CHUNK_SIZE_PIXELS, CHUNK_SIZE_TILES

def pix_to_tile(coord):

    return round_coord((coord[0]//TILE_SIZE_PIXELS, coord[1]//TILE_SIZE_PIXELS))

def pix_to_chunk(coord):

    return round_coord((coord[0]//CHUNK_SIZE_PIXELS, coord[1]//CHUNK_SIZE_PIXELS))

def tile_to_chunk(coord):

    return round_coord((coord[0]//CHUNK_SIZE_TILES, coord[1]//CHUNK_SIZE_TILES))

def tile_to_tileref(coord): # CHUNK + TILE POS WITHIN CHUNK
    div = divmod(coord[0], CHUNK_SIZE_TILES), divmod(coord[1], CHUNK_SIZE_TILES)
    return (div[0][0], div[1][0]), (div[0][1], div[1][1])

def pix_to_tileref(coord):

    return tile_to_tileref(pix_to_tile(coord))

def coord_range(A, B):

    return [(x,y) for x in range(A[0],B[0]) for y in range(A[1], B[1])]

def round_coord(coord):

    return (int(coord[0]), int(coord[1]))