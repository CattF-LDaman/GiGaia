
from GiGaia.GiCore.Data.datafile import Datafile
from GiGaia.GiCore.Data.datatypes import D_TILES, D_STRING, D_INT128, D_POS

from GiGaia.GiCore.Game.World.coords import sum_coords, sub_coords, inside

import os
import time

class StructureData(Datafile):

    DATA_VERSION = 1
    STRUC = (
            ("author", D_STRING, 1),
            ("description", D_STRING, 2),
            ("time_created", D_INT128),
            ("tiles", D_TILES, 12),
            ("core", D_POS)
            )


    def __init__(self, location):

        super().__init__(location)
    
    def on_create(self, world, start, end, core=(0,0), author="Anonymous", description="No description."):

        self.time_created = int(time.time())
        self.author = author
        self.description = description

        self.tiles = [[], []]
        for l, layer in enumerate(self.tiles):
            for y in range(start[1]-1, end[1]):
                layer.append(row := [])
                for x in range(start[0], end[0]+1):
                    row.append(world.get_at(x,y,l))

        self.core = core

    def get_at(self, x, y, z, wcore):
        """
        Retrieve data at the specified coordinates and layer relative to the structure core.
        :param x: X-coordinate relative to the structure core.
        :param y: Y-coordinate relative to the structure core.
        :param z: Layer index.
        :param wcore: World core coordinates.
        :return: Data at the specified position.
        """
        # Calculate relative coordinates based on the structure core and wcore
        rel_x, rel_y = sub_coords((x, y), wcore)

        # Calculate the aligned position within the structure's grid
        aligned_x, aligned_y = sum_coords((rel_x, rel_y), self.core)

        # Access the specified layer
        layer = self.tiles[z]

        # If the provided coordinates are within the valid range
        if 0 <= aligned_x < len(layer[0]) and 0 <= aligned_y < len(layer):
            return layer[aligned_y][aligned_x]
        else:
            # Handle out-of-bounds coordinates (returning a default value or raising an exception)
            return None

    def calculate_bounds(self, wcore):
        """
        Calculate the world coordinates for the top-left and bottom-right corners of the structure.
        :param wcore: World core coordinates.
        :return: Tuple of top-left and bottom-right world coordinates.
        """
        # Calculate relative position within the structure's grid
        rel_x, rel_y = sub_coords((0, 0), self.core)

        # Calculate the top-left and bottom-right corners in the world
        top_left = sum_coords((rel_x, rel_y), wcore)
        bottom_right = sum_coords((rel_x + len(self.tiles[0][0]), rel_y + len(self.tiles[0])), wcore)

        return top_left, bottom_right
    
    @property
    def width(self):
        return len(self.tiles[0][0])
    
    @property
    def height(self):
        return len(self.tiles[0])

    def within(self, point, wcore):

        return inside(point, *self.calculate_bounds(wcore))