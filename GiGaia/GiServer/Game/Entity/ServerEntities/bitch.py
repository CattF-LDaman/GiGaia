
from .physical import Physical
from GiGaia.GiCore.Game.Entities import Bitch as BitchBase

import math
import random

class Bitch(Physical, BitchBase):

    BITCH_PHYSICS = {
        "mass": 0,
        "width": 2,
        "height": 2,
        "friction": 0,
        "air_friction": 5,
    }

    SPEED = 2000

    def __init__(self, entity_manager, eid, position, props):
        
        props.update(self.BITCH_PHYSICS)

        super().__init__(entity_manager, eid, position, props)

        col = random.randint(1,20)
        self.change("color", (col, col, col))

    def tick(self):

        self.add_velocity(random.uniform(-self.SPEED,self.SPEED),random.uniform(-self.SPEED,self.SPEED))

        #self.change("color", (random.randint(0,255),random.randint(0,255),random.randint(0,255)))

        self.update_physics()