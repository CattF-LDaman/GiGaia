
from GiGaia.GiCore.Data.datafile import Datafile
from GiGaia.GiCore.Data.datatypes import D_DEC, D_RGI, D_INT128, D_INT64

from GiGaia.GiCore.Game.World import REGION_SIZE_CHUNKS
from GiGaia.GiCore.Game.World.coords import chunk_region

import os
import pygame

pygame.init()

class WDataViz:

    def __init__(self, worlds_dir, world_name, out):

        self.worlds_dir = worlds_dir
        self.world_name = world_name

        self.data = WorldData(self.worlds_dir, self.world_name)

        self.out = out

        self.width = 10000
        self.height = 5000
        self.offset_x = int(self.width/2)
        self.offset_y = 200

        self.surf = pygame.Surface((self.width, self.height))
        self.p = pygame.PixelArray(self.surf)

        print(f"{self.width}x{self.height} {self.world_name} @ {self.worlds_dir} -> {self.out}")

        self.visualize()

    def visualize(self):

        for rp in self.data.existing_region_files:
            r_data = self.data.get_region(rp)
            for cp in r_data.rgi.keys():
                print(cp)
                draw_pos = cp[0]+self.offset_x, cp[1]+self.offset_y
                if draw_pos[0] < 0 or draw_pos[1] < 0:
                    continue
                if draw_pos[0] > self.width-1 or draw_pos[1] > self.height-1:
                    continue
                self.p[draw_pos[0], draw_pos[1]] = (255,255,255)

        pygame.image.save(self.surf, self.out)

class WorldData(Datafile):
    AUTO_CREATE = False

    DATA_VERSION = 2
    STRUC = (
            ("seed", D_INT64),
            ("time_created", D_INT128),
            ("last_saved",D_INT128),
            ("game_time", D_DEC)
            )

    def __init__(self, worlds_dir, worldname):

        self.world_location = os.path.join(worlds_dir, worldname)
        
        self.region_files = {}
        self.region_dir = os.path.join(self.world_location, "regions")

        self.existing_region_files = []
        for rfn in os.listdir(self.region_dir):
            if (parsed_rfn := self.parse_region_filename(rfn)):
                self.existing_region_files.append(parsed_rfn)

        super().__init__(os.path.join(self.world_location,worldname+'.world'))

        self.save = None
    
    def get_chunk(self, cp):

        cr = chunk_region(cp)

        if not self.has_region(cr):
            return None
        
        return self.get_region(cr).get_chunk(cp)
    
    def has_chunk(self, cp):

        cr = chunk_region(cp)

        if not self.has_region(cr):
            return False
        
        return self.get_region(cr).has_chunk(cp)
        
    def get_region(self, rp):

        if rp in self.region_files:
            return self.region_files[rp]
        
        elif rp in self.existing_region_files:
            self.create_region_file(rp)
            return self.region_files[rp]

        return None

    def has_region(self, rp):

        return rp in self.region_files or rp in self.existing_region_files

    def parse_region_filename(self, name):
        try:

            posh = name.split(".")[0]
            xb = bytes.fromhex(posh[:24])
            yb = bytes.fromhex(posh[24:])
            x = int.from_bytes(xb, "little", signed=True)
            y = int.from_bytes(yb, "little", signed=True)

            return (x,y)

        except Exception:
            return False

    def create_region_file(self, region_pos):

        try:
            self.region_files[region_pos] = RegionData(self, region_pos)
        except Exception:
            pass

class RegionData(Datafile):

    AUTO_CREATE = False

    DATA_VERSION = 1
    STRUC = (
            ("rgi", D_RGI, 8),
            )
    
    def __init__(self, worlddata, region_pos):

        self.region_pos = region_pos

        try:
            super().__init__(os.path.join(worlddata.world_location, "regions", self.name))
        except Exception:
            os.remove(os.path.join(worlddata.world_location, "regions", self.name))
            super().__init__(os.path.join(worlddata.world_location, "regions", self.name))

    @property
    def name(self):
        x = self.region_pos[0].to_bytes(12, "little", signed=True).hex()
        y = self.region_pos[1].to_bytes(12, "little", signed=True).hex()
        return x+y+".rgi"
    
    def has_chunk(self, cp):

        return cp in self.rgi
    
    def get_chunk(self, cp):
        
        if self.has_chunk(cp):
            return self.rgi[cp]
        return None

if __name__ == "__main__":

    ws_dir = input("WORLDS_DIRECTORY: ")
    w_name = input("WORLD_NAME: ")
    out = input("OUT: ")
    WDataViz(ws_dir, w_name, out)