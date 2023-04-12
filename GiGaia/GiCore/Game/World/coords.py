
from . import TILE_SIZE_PIXELS, CHUNK_SIZE_PIXELS, CHUNK_SIZE_TILES

def pix_to_tile(coord):

    return (int(coord[0]/TILE_SIZE_PIXELS), int(coord[1]/TILE_SIZE_PIXELS))

def pix_to_chunk(coord):

    return (int(coord[0]/CHUNK_SIZE_PIXELS), int(coord[1]/CHUNK_SIZE_PIXELS))

def tile_to_chunk(coord):

    return (int(coord[0]/CHUNK_SIZE_TILES), int(coord[1]/CHUNK_SIZE_TILES))

def tile_to_tileref(coord): # CHUNK + TILE POS WITHIN CHUNK
    div = divmod(coord[0], CHUNK_SIZE_TILES), divmod(coord[1], CHUNK_SIZE_TILES)
    return (div[0][0], div[1][0]), (div[0][1], div[1][1])

def pix_to_tileref(coord):

    return tile_to_tileref(pix_to_tile(coord))