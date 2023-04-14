
from .entity import Entity
from GiGaia.GiCore.Game.Entities import Bob as BobBase

import random

class Bob(Entity, BobBase):

    def __init__(self, entity_manager, eid, position, props):
        
        super().__init__(entity_manager, eid, position, props)

    def add_coins(self, amount):

        self.change("coins", self.props["coins"]+amount)

    def tick(self):

        self.position[0] += random.uniform(-1,1)*self.game.dt