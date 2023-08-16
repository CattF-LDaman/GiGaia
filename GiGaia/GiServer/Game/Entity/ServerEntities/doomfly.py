
from .physical import Physical
from GiGaia.GiCore.Game.Entities import Doomfly as DoomflyBase

import math
import random

class Doomfly(Physical, DoomflyBase):

    FIREFLY_PHYSICS = {
        "mass": 0,
        "width": 2,
        "height": 2,
        "friction": 0,
        "air_friction": 5,
    }

    SPEED_X = 3000
    SPEED_Y = 1100

    REST_DURATION = 2000
    REST_COOLDOWN = 4000

    def __init__(self, entity_manager, eid, position, props):
        
        props.update(self.FIREFLY_PHYSICS)

        super().__init__(entity_manager, eid, position, props)

        col = random.randint(1,20)
        self.change("color", (col, col, col))

        self.last_rest = 0

    def tick(self):

        if self.props["resting"] and self.game.ticks > self.props["resting"]:
            self.last_rest = self.props["resting"]
            self.change("resting", 0)
            #self.resting = False

        if not self.props["resting"]:

            self.add_velocity(random.uniform(-self.SPEED_X,self.SPEED_X),random.uniform(-self.SPEED_Y,self.SPEED_Y))

            #self.change("color", (random.randint(0,255),random.randint(0,255),random.randint(0,255)))

            self.update_physics()

            if (self.hugging or self.grounded) and self.game.ticks > self.last_rest+self.REST_COOLDOWN:

                self.change("resting", self.game.ticks+self.REST_DURATION)
                self.set_velocity(0, 0)