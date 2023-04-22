
from GiGaia.GiCore.Data.datafile import Datafile
from GiGaia.GiCore.Data.datatypes import D_INT64, D_RGI, D_CHUNK
from GiGaia.GiCore.Data.hashing import hash_pwd, hash_str

from GiGaia.GiCore.Game.World.coords import chunk_region

import os
import time

class WorldData(Datafile):
    AUTO_CREATE = True

    DATA_VERSION = 1
    STRUC = (
            ("seed", D_INT64),
            ("time_created", D_INT64),
            ("last_saved",D_INT64)
            )


    def __init__(self, worlds_dir, worldname, world):

        self.world = world

        self.world_location = os.path.join(worlds_dir, worldname)
        
        self.region_files = {}
        self.region_dir = os.path.join(self.world_location, "regions")

        os.makedirs(self.region_dir, exist_ok=True)

        self.existing_region_files = []
        for rfn in os.listdir(self.region_dir):
            if (parsed_rfn := self.parse_region_filename(rfn)):
                self.existing_region_files.append(parsed_rfn)

        super().__init__(os.path.join(self.world_location,worldname+'.world'))
    
    def get_chunk(self, cp):

        cr = chunk_region(cp)

        if not self.has_region(cr):
            return None
        
        return self.get_region(cr).get_chunk(cp)
        
    def get_region(self, rp):

        if rp in self.region_files:
            return self.region_files[rp]
        
        elif rp in self.existing_region_files:
            if rp not in self.world.regions:
                self.world.create_region(rp)
            self.create_region_file(self.world.regions[rp])
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

    def on_create(self, seed=int.from_bytes(os.urandom(8), "little")):

        self.seed = seed
        self.time_created = int(time.time())

    def create_region_file(self, region):

        self.region_files[region.position] = RegionData(self, region)

    def on_save(self):
        
        for region_pos,region in self.world.regions.items():
            if region_pos not in self.region_files:
                self.create_region_file(region)
            self.region_files[region_pos].save()

        self.last_saved = int(time.time())

class RegionData(Datafile):

    AUTO_CREATE = True

    DATA_VERSION = 1
    STRUC = (
            ("rgi", D_RGI, 8),
            )
    
    def __init__(self, worlddata, region):

        self.region = region

        super().__init__(os.path.join(worlddata.world_location, "regions", self.name))

    @property
    def name(self):
        x = self.region.position[0].to_bytes(12, "little", signed=True).hex()
        y = self.region.position[1].to_bytes(12, "little", signed=True).hex()
        return x+y+".rgi"
    
    def has_chunk(self, cp):

        return cp in self.rgi
    
    def get_chunk(self, cp):
        
        if self.has_chunk(cp):
            return self.rgi[cp]
        return None

    def update_rgi(self):

        rgi_data = {}
        for chunk_pos, chunk in self.region.chunks.items():
            if chunk.modified:
                rgi_data[chunk_pos] = chunk.tiles
                chunk.modified = False
        self.rgi.update(rgi_data)
    
    def on_save(self):
        
        self.update_rgi()

    def on_create(self):

        self.rgi = {}
        self.update_rgi()
