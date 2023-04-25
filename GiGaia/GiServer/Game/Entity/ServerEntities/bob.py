
from .physical import Physical
from GiGaia.GiCore.Game.Entities import Bob as BobBase

import math
import random

class Bob(Physical, BobBase):

    BOB_PHYSICS = {
        "mass": 95,
        "width": 8,
        "height": 8,
        "friction": 10,
        "air_friction": 10,
    }

    RANDOM_QUOTES = ["I'm gonna fuck you up!","Come here you bitch!","Kgan al je tandn der ut slan!"]

    SPEED = 3000
    JUMP = 560
    DETECT_RANGE = 1000

    QUOTE_EVERY = 1000

    def __init__(self, entity_manager, eid, position, props):
        
        props.update(self.BOB_PHYSICS)

        super().__init__(entity_manager, eid, position, props)

        self.last_quote = 0

    def add_coins(self, amount):

        self.change("coins", self.props["coins"]+amount)

    def move(self, movement):

        mx = movement

        self.add_velocity(mx*self.SPEED if self.grounded else mx*self.SPEED)

    def jump(self):

        self.set_velocity(y=-self.JUMP if self.grounded else None)

    def decide(self):

        closest = [None, self.DETECT_RANGE]
        for p in self.game.players.values():
            if p.entity:
                if (p_dist := math.dist(self.position, p.entity.position)) < closest[1]:
                    closest[0] = p.entity
                    closest[1] = p_dist

        if closest[0]:
            direction = 1 if closest[0].position[0] > self.position[0] else -1
            self.move(direction)

            if closest[0].position[1] < self.position[1]:
                self.jump()

        if self.hugging:
            self.jump()

    def tick(self):

        self.decide()

        if self.game.ticks - self.last_quote > self.QUOTE_EVERY:
            self.change("name", random.choice(self.RANDOM_QUOTES))
            self.last_quote = self.game.ticks

        self.update_physics()