
from .chunk import Chunk

class Region:

    def __init__(self, world, pos):
        
        self.world = world
        self.position = pos

        self.chunks = {}

    def create_chunk(self, chunk_pos):

        self.chunks[chunk_pos] = Chunk(self, chunk_pos)
