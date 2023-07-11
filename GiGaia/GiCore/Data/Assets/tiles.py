
from GiGaia.GiCore.random_util import seeded_randchoice
from GiGaia.GiCore.Game.World import TILE_SPRITE_SIZE
from GiGaia.GiCore.sprite_util import rotate, replace_color

from types import SimpleNamespace
import pygame
import os

DARKNESS = (30,30,15)

def load_shapes(man):

    loc = os.path.join(man.location,"TileShapes")
    shape_assets = [(s, os.path.join(loc, s)) for s in os.listdir(loc)]

    shapes = {}

    for shape_name, shape in shape_assets:
        if os.path.isdir(shape):
            shapes[shape_name] = TileShape(man, shape)

    man.tile_shapes = shapes

def load(man):
    """
    TIDS.DIRT = 1
    TILES.DIRT = Tile()
    tile_name_by_id[1] = "dirt"
    tiles[1] = Tile()
    tile_names["DIRT"] = Tile()
    tile_ids["DIRT"] = 1
    """
    man.instance.log("[ASSETS] Loading tiles...")

    data = man.assets["data"]

    load_shapes(man)

    tile_names_id = {}
    for tile_id, tile_name in enumerate(data.tiles):
        
        tile_names_id[tile_id+1] = tile_name

    tile_ids = {tn.upper():tid for tid, tn in tile_names_id.items()}
    tiles = {tid:Tile(man, tid, tn, data.Tiles.__dict__[tn]) for tid, tn in tile_names_id.items()}
    tile_names = {tile_names_id[tid].upper():t for tid, t in tiles.items()}

    man.TIDS = SimpleNamespace(**tile_ids)
    man.TILES = SimpleNamespace(**tile_names)
    man.tile_ids = tile_ids
    man.tile_name_by_id = tile_names_id
    man.tiles = tiles
    man.tile_names = tile_names

class Tile:

    DEFAULTS = {
    "display": "NaN",
    "sprite": {
        "shape": "Dirty",
        "components": {
            "base": [0, 0, 0],
            "grain": [0, 0, 0],
            "border": [0, 0, 0]
                    }
            },

    "platform": False,

    "alike": ()
    }

    def __init__(self, man, tid, tname, tile_data):

        tile_data = {**self.DEFAULTS, **tile_data}

        self.id = tid
        self.name = tname

        self.display_name = tile_data["display"]
        self.color = tile_data["sprite"] # TEMPORARY

        self.sprite_shape = tile_data["sprite"]["shape"]
        self.sprite_components = tile_data["sprite"]["components"]

        self.is_platform = tile_data["platform"]

        self.alike = tile_data["alike"]

        self.shape = man.tile_shapes[self.sprite_shape]
    
    def _trbl_filter(self, t):
        if t in self.alike:
            return 1
        match t:
            case self.id:
                return 1
            case 0:
                return 0
            case _:
                return 2

    def get_sprite(self, trbl, depth=0, trand=0):
        
        #tsp = pygame.Surface((TILE_SPRITE_SIZE, TILE_SPRITE_SIZE))
        #tsp.fill(darken(self.color, depth*30))

        trbl = [self._trbl_filter(v) for v in trbl]
        tsp = self.shape.get_tile(self.sprite_components, trbl, depth, trand)

        return tsp
    
class TileShape:

    def __init__(self, man, loc):
        
        self.man = man

        self.name = os.path.basename(loc)
        self.location = loc

        self.data = self.man.assets["data"].TileShapes.__dict__[self.name.lower()]
        self.components = self.data["components"]

        self.types = {"empty":None, "full":None, "one":None, "three":None, "twoc":None, "twop":None}
        self.sprites = {}

        self._load()

    def _load(self):

        for ttype in self.types:
            type_img = pygame.image.load(os.path.join(self.location, ttype+".png"))
            self.types[ttype] = self._load_type_img(type_img)

    def _load_type_img(self, type_img):

        sr = pygame.Rect(0, 0, TILE_SPRITE_SIZE, TILE_SPRITE_SIZE)
        sprites = []

        for sn in range(type_img.get_width()//TILE_SPRITE_SIZE):
            sr.topleft = (TILE_SPRITE_SIZE*sn, 0)
            sprites.append(type_img.subsurface(sr))

        return sprites

    def get_type_rot(self, trbl):

        match trbl:

            case (0,0,0,0):
                return ("empty", 0)
            
            case (0,0,0,1):
                return ("one", 180)
            
            case (0,0,1,0):
                return ("one", 90)
            
            case (0,0,1,1):
                return ("twoc", 90)
            
            case (0,1,0,0):
                return ("one", 0)
            
            case (0,1,0,1):
                return ("twop", 0)
            
            case (0,1,1,0):
                return ("twoc", 0)
            
            case (0,1,1,1):
                return ("three", 0)
            
            case (1,0,0,0):
                return ("one", 270)
            
            case (1,0,0,1):
                return ("twoc", 180)
            
            case (1,0,1,0):
                return ("twop", 90)
            
            case (1,0,1,1):
                return ("three", 90)
            
            case (1,1,0,0):
                return ("twoc", 270)
            
            case (1,1,0,1):
                return ("three", 180)
            
            case (1,1,1,0):
                return ("three",270)
            
            case (1,1,1,1):
                return ("full",0)

    def get_type_rot_sprite(self, ttype, rot, rnd=12345):
        if ttype not in self.sprites:
            self.sprites[ttype] = {}

        if rot not in self.sprites[ttype]:
            self.sprites[ttype][rot] = []
            for t_img in self.types[ttype]:
                self.sprites[ttype][rot].append(rotate(t_img, rot))

        return seeded_randchoice(self.sprites[ttype][rot], rnd)

    def get_type_sprite(self, trbl, rnd=12345):

        tr_IN = tuple(v if v != 2 else 1 for v in trbl)

        ttype, rot = self.get_type_rot(tr_IN)
        return self.get_type_rot_sprite(ttype, rot, rnd)

    def get_tile(self, components, trbl, dark=False, rnd=12345):

        shape = self.get_type_sprite(trbl, rnd).copy()
        
        for compname, compcolor in self.components.items():
            if compname in components:
                replace_color(shape, compcolor, components[compname])

        if "border" in components:
            if trbl[0] == 2:
                pygame.draw.line(shape, components["border"], (0,0), (TILE_SPRITE_SIZE-1, 0))
            if trbl[1] == 2:
                pygame.draw.line(shape, components["border"], (TILE_SPRITE_SIZE-1, 0), (TILE_SPRITE_SIZE-1, TILE_SPRITE_SIZE-1))
            if trbl[2] == 2:
                pygame.draw.line(shape, components["border"], (0, TILE_SPRITE_SIZE-1), (TILE_SPRITE_SIZE-1, TILE_SPRITE_SIZE-1))
            if trbl[3] == 2:
                pygame.draw.line(shape, components["border"], (0, TILE_SPRITE_SIZE-1), (0, 0))

        if dark:
            shape.fill(DARKNESS, special_flags=pygame.BLEND_RGB_SUB)

        return shape


