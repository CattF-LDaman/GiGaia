
from .physical import Physical
from GiGaia.GiCore.Game.Entities import Bitch as BitchBase

import math
import random

class Bitch(Physical, BitchBase):

    BITCH_PHYSICS = {
        "mass": 0,
        "width": 8,
        "height": 8,
        "friction": 0,
        "air_friction": 5,
    }

    SPEED = 3000
    JUMP = 560

    def __init__(self, entity_manager, eid, position, props):
        
        props.update(self.BITCH_PHYSICS)

        super().__init__(entity_manager, eid, position, props)

    def tick(self):

        self.add_velocity(random.uniform(-2000,2000),random.uniform(-2000,2000))

        #self.change("color", (random.randint(0,255),random.randint(0,255),random.randint(0,255)))

        self.update_physics()