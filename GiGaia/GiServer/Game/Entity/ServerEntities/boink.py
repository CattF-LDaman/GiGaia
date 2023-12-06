
from .physical import Physical
from GiGaia.GiCore.Game.Entities import Boink as BoinkBase

import math
import random

class Boink(Physical, BoinkBase):

    BOINK_PHYSICS = {
        "mass": 50,
        "width": 12,
        "height": 12,
        "friction": 8,
        "air_friction": 10,
    }

    SPEED = 3500
    JUMP = 600
    DETECT_RANGE = 80
    MIN_RANGE = 20
    CHANGE_DIR_EVERY = 4000
    STROLL_DURATION = 2000
    IDLE_DURATION = 3000

    def __init__(self, entity_manager, eid, position, props):
        
        props.update(self.BOINK_PHYSICS)

        super().__init__(entity_manager, eid, position, props)

        self.step_up = True

        self.last_chdir = 0
        self.direction = 1
        self.strolling_start = self.game.ticks - ((self.STROLL_DURATION+self.IDLE_DURATION)*random.uniform(0,1))

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
                    if p_dist > self.MIN_RANGE:
                        closest[0] = p.entity
                        closest[1] = p_dist

        if closest[0]:
            direction = 1 if closest[0].position[0] > self.position[0] else -1
            self.move(direction)

        else:
            if self.game.ticks - self.last_chdir > self.CHANGE_DIR_EVERY:
                self.direction = random.choice([-1, 1])
                self.last_chdir = self.game.ticks
            
            if self.game.ticks - self.strolling_start < self.STROLL_DURATION:
                self.move(self.direction)
            if self.game.ticks - self.strolling_start > self.STROLL_DURATION + self.IDLE_DURATION:
                self.strolling_start = self.game.ticks

        if self.hugging:
            self.last_chdir = 0
            self.jump()

    def tick(self):

        self.decide()
        self.update_physics()