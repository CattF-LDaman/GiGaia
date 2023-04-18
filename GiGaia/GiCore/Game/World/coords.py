
from . import TILE_SIZE_PIXELS, CHUNK_SIZE_PIXELS, CHUNK_SIZE_TILES, REGION_SIZE_CHUNKS

def chunk_region(coord):

    return round_coord((coord[0]//REGION_SIZE_CHUNKS, coord[1]//REGION_SIZE_CHUNKS))

def pix_to_tile(coord):

    return round_coord((coord[0]//TILE_SIZE_PIXELS, coord[1]//TILE_SIZE_PIXELS))

def pix_to_chunk(coord):

    return round_coord((coord[0]//CHUNK_SIZE_PIXELS, coord[1]//CHUNK_SIZE_PIXELS))

def tile_to_chunk(coord):

    return round_coord((coord[0]//CHUNK_SIZE_TILES, coord[1]//CHUNK_SIZE_TILES))

def chunk_to_tile(coord):

    return mult_coord(coord, CHUNK_SIZE_TILES)

def chunk_to_pix(coord):

    return tile_to_pix(chunk_to_tile(coord))

def tile_to_pix(coord):

    return mult_coord(coord, TILE_SIZE_PIXELS)

def chunk_tile_positions(coord):
    
    chunk_tile_pos = chunk_to_tile(coord)
    return coord_range(chunk_tile_pos, (chunk_tile_pos[0]+CHUNK_SIZE_TILES, chunk_tile_pos[1]+CHUNK_SIZE_TILES))

def tileref_to_tile(coord):

    return sum_coords(chunk_to_tile(coord[0]), coord[1])

def tile_to_tileref(coord): # CHUNK + TILE POS WITHIN CHUNK
    div = divmod(coord[0], CHUNK_SIZE_TILES), divmod(coord[1], CHUNK_SIZE_TILES)
    return (div[0][0], div[1][0]), (div[0][1], div[1][1])

def pix_to_tileref(coord):

    return tile_to_tileref(pix_to_tile(coord))

def coord_range(A, B):

    return [(x,y) for x in range(A[0],B[0]) for y in range(A[1], B[1])]

def coord_square(C , r):

    return coord_range((C[0]-r,C[1]-r), (C[0]+r, C[1]+r))

def round_coord(coord):

    return (int(coord[0]), int(coord[1]))

def sum_coords(*coords):

    return (sum(c[0] for c in coords), sum(c[1] for c in coords))

def mult_coord(coord, mult):
    
    return (coord[0]*mult, coord[1]*mult)

def add_coord(coord, add):

    return (coord[0]+add, coord[1]+add)