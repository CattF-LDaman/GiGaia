
from GiGaia.GiCore.Data.datafile import Datafile
from GiGaia.GiCore.Data.datatypes import D_INT64, D_RGI, D_CHUNK
from GiGaia.GiCore.Data.hashing import hash_pwd, hash_str

import os
import time

class WorldData(Datafile):
    AUTO_CREATE = True

    DATA_VERSION = 1
    STRUC = (
            #("chunk", D_CHUNK),
            ("seed", D_INT64),
            ("time_created", D_INT64),
            ("last_saved",D_INT64)
            )


    def __init__(self, worlds_dir, worldname, world):

        self.world = world

        self.world_location = os.path.join(worlds_dir, worldname)
        
        self.region_files = {}

        os.makedirs(os.path.join(self.world_location, "regions"), exist_ok=True)

        super().__init__(os.path.join(self.world_location,worldname+'.world'))
    
    def on_create(self, seed=int.from_bytes(os.urandom(8), "little")):

        self.seed = seed
        self.time_created = int(time.time())

    def create_region_file(self, region):

        self.region_files[region.position] = RegionData(self, region)

    def on_save(self):
        
        for region_pos,region in self.world.regions.items():
            if region_pos not in self.region_files:
                self.create_region_file(region)

        self.last_saved = int(time.time())

class RegionData(Datafile):

    AUTO_CREATE = True

    DATA_VERSION = 1
    STRUC = (
            ("rgi", D_RGI),
            )
    
    def __init__(self, worlddata, region):

        self.region = region

        super().__init__(os.path.join(worlddata.world_location, self.name))

    @property
    def name(self):
        x = self.region.position[0].to_bytes(12, "little").hex()
        y = self.region.position[1].to_bytes(12, "little").hex()
        return x+y+".rgi"
    
    @property
    def chunk_struc(self):

        struc = []
        for chunk_pos in self.region.chunks:
            struc.append((chunk_pos, D_CHUNK))
        return struc

    def update_rgi(self):

        self.rgi = [self.chunk_struc, [chunk.tiles for chunk in self.region.chunks]]

    def on_create(self):

        self.update_rgi()
        self.seed = seed