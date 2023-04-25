
from .entity import Entity
from GiGaia.GiCore.Game.Entities import Physical as PhysicalBase

from GiGaia.GiCore.Game.World.coords import pix_chunk_range, round_coord
from GiGaia.GiCore.Game.World import TILE_SIZE_PIXELS

import random
import pygame

class Physical(Entity, PhysicalBase):

    def __init__(self, entity_manager, eid, position, props):
        
        super().__init__(entity_manager, eid, position, props)

        self.velocity = [0, 0]

        self.rect = pygame.Rect(0,0,self.props["width"],self.props["height"])
        self.check_rect = pygame.Rect(0,0,self.props["width"]+(TILE_SIZE_PIXELS*2),self.props["height"]+(TILE_SIZE_PIXELS*2))

        self.grounded = False
        self.hugging = False

    def aids(self):
        return pix_chunk_range(self.check_rect.topleft, self.check_rect.bottomright)

    def _check_collision(self):

        for chunk in self.game.world.grab_all(pix_chunk_range(self.check_rect.topleft, self.check_rect.bottomright)):
            if not chunk:
                return True
            for col_rect in chunk.get_collision():
                if col_rect.colliderect(self.rect):
                    return col_rect
        return False

    def update_physics(self):

        self.grounded = self.hugging = False

        dt = self.game.dt
        vel_x, vel_y = self.velocity #self.props["vel"]
        mov_x, mov_y = vel_x*dt, vel_y*dt

        prev_x, prev_y = self.position

        self.position[0] += mov_x
        self.rect.center = self.position
        self.check_rect.center = self.position

        if (col := self._check_collision()):
            self.position[0] = prev_x
            vel_x = 0
            self.hugging = True
        
        self.position[1] += mov_y
        self.rect.center = self.position
        self.check_rect.center = self.position

        if (col := self._check_collision()):
            if vel_y > 0:
                self.grounded = True
            self.position[1] = prev_y
            vel_y = 0
            vel_x *= 1 / (1 + (dt * self.props["friction"])) #*= self.props["friction"]**(dt*60)
        else:
            vel_x *= 1 / (1 + (dt * self.props["air_friction"]))

        grav = TILE_SIZE_PIXELS*dt*2*self.props["mass"]

        nvel = round_coord((vel_x, vel_y+grav), 2)
        self.velocity = nvel
        #self.change("vel", nvel)
        
    def set_velocity(self, x=None, y=None):

        #self.change("vel", (x if x is not None else self.props["vel"][0], y if y is not None else self.props["vel"][1]))
        self.velocity = (x if x is not None else self.velocity[0], y if y is not None else self.velocity[1])

    def add_velocity(self, x=None, y=None):

        #vel_x, vel_y = self.props["vel"]
        #self.change("vel", (vel_x+(x*self.game.dt) if x is not None else vel_x, vel_y+(y*self.game.dt) if y is not None else vel_y))
        vel_x, vel_y = self.velocity
        self.velocity = (vel_x+(x*self.game.dt) if x is not None else vel_x, vel_y+(y*self.game.dt) if y is not None else vel_y)

    def tick(self):

        pass