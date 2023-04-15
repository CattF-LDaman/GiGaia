
from GiGaia.GiCore.Game.World.coords import pix_to_chunk, pix_to_tile

from GiGaia.GiCore.Data.datatypes import D_STRING

class Entity:

    ID = 0
    NAME = "BaseEntity"
    PROPERTIES = {
        ("name", D_STRING, 1): ""
    }

    def __init__(self, eid, position=(0,0)):
        
        self.instance_id = self.eid = eid
        self.position = list(position)

        if hasattr(self.__class__,'PROPERTIES'):
            for cls in self.__class__.__mro__:  # Merges properties between child and parent classes
                if cls != self.__class__:
                    self.__class__.PROPERTIES.update(getattr(cls,'PROPERTIES',[])) #self.__class__.PROPERTIES.extend(getattr(cls,'PROPERTIES',[]))

        self.props = {}

    def set_properties(self, props):

        self.props = {**{p[0]:default for p, default in self.PROPERTIES.items()}, **props}

    @property
    def identity_str(self):

        return f"{self.NAME} ({self.ID}): #{self.eid} @({self.position[0]}, {self.position[1]})"
    
    @property
    def chunk_pos(self):

        return pix_to_chunk(self.position)
    
    @property
    def tile_pos(self):

        return pix_to_tile(self.position)
