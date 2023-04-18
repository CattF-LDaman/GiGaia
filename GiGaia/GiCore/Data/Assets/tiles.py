
from GiGaia.GiCore.random_util import seeded_randchoice
from GiGaia.GiCore.Game.World import TILE_SPRITE_SIZE
from GiGaia.GiCore.color_util import darken

from types import SimpleNamespace
import pygame

def load(man):
    """
    TIDS.DIRT = 1
    TILES.DIRT = Tile()
    tile_name_by_id[1] = "dirt"
    tiles[1] = Tile()
    tile_names["DIRT"] = Tile()
    tile_ids["DIRT"] = 1
    """
    data = man.assets["data"]

    tile_names_id = {}
    for tile_id, tile_name in enumerate(data.tiles):
        
        tile_names_id[tile_id+1] = tile_name

    tile_ids = {tn.upper():tid for tid, tn in tile_names_id.items()}
    tiles = {tid:Tile(tid, tn, data.Tiles.__dict__[tn]) for tid, tn in tile_names_id.items()}
    tile_names = {tile_names_id[tid].upper():t for tid, t in tiles.items()}

    man.TIDS = SimpleNamespace(**tile_ids)
    man.TILES = SimpleNamespace(**tile_names)
    man.tile_ids = tile_ids
    man.tile_name_by_id = tile_names_id
    man.tiles = tiles
    man.tile_names = tile_names

class Tile:

    def __init__(self, tid, tname, tile_data):

        self.id = tid
        self.name = tname

        self.display_name = tile_data["display"]
        self.color = tile_data["sprite"] # TEMPORARY
    
    def get_sprite(self, depth=0, trand=0):
        
        tsp = pygame.Surface((TILE_SPRITE_SIZE, TILE_SPRITE_SIZE))
        tsp.fill(darken(self.color, depth*30))

        return tsp