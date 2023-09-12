
from .physical import Physical
from GiGaia.GiCore.Game.Entities import ItemEntity as ItemEntityBase

import math

class ItemEntity(Physical, ItemEntityBase):

    ITM_PHYSICS = {
        "mass": 50,
        "width": 9,
        "height": 9,
        "friction": 10,
        "air_friction": 10,
    }

    FLY_RANGE = 55
    PICKUP_RANGE = 8
    FLY_SPEED = 2000

    def __init__(self, entity_manager, eid, position, props):
        
        props.update(self.ITM_PHYSICS)

        super().__init__(entity_manager, eid, position, props)

    def tick(self):

        closest = [None, self.FLY_RANGE]
        for p in self.seen_by:
            if p.entity:
                if (p_dist := math.dist(self.position, p.entity.position)) < closest[1]:
                    closest[0] = p.entity
                    closest[1] = p_dist

        if (ent := closest[0]):
            self.change("mass", 0)
            self.add_velocity(self.FLY_SPEED*(-1 if ent.position[0]<self.position[0] else 1), self.FLY_SPEED*(-1 if ent.position[1]<self.position[1] else 1))
            if closest[1] < self.PICKUP_RANGE and p.inv.has_space("person", self.props["amount"]):
                p.play_sound("plop")
                p.inv.add_item("person", self.props["item"], self.props["amount"])
                self.destroy()
        else:
            self.change("mass", self.ITM_PHYSICS["mass"])

        self.update_physics()