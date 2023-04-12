
from GiGaia.GiCore.Game.World.coords import pix_to_chunk, pix_to_tile

class Entity:

    ID = 0
    NAME = "BaseEntity"
    PROPERTIES = ()

    def __init__(self, eid, position=(0,0)):
        
        self.instance_id = self.eid = eid
        self.position = list(position)

    @property
    def identity(self):

        return f"{self.NAME} ({self.ID}): {self.eid}"
    
    @property
    def chunk_pos(self):

        return pix_to_chunk(self.position)
    
    @property
    def tile_pos(self):

        return pix_to_tile(self.position)
    
