
from .entity import Entity
from GiGaia.GiCore.Game.Entities import Physical as PhysicalBase

from GiGaia.GiCore.Game.World.coords import pix_chunk_range, round_coord
from GiGaia.GiCore.Game.World import TILE_SIZE_PIXELS

import math
import pygame

class Physical(Entity, PhysicalBase):

    def __init__(self, entity_manager, eid, position, props):
        
        super().__init__(entity_manager, eid, position, props)

        self.velocity = [0, 0]

        self.rect = pygame.Rect(0,0,self.props["width"],self.props["height"])
        self.check_rect = pygame.Rect(0,0,self.props["width"]+(TILE_SIZE_PIXELS*2),self.props["height"]+(TILE_SIZE_PIXELS*2))

        self.grounded = False
        self.hugging = False

        self.ghost_platforms = False
        self.step_up = False

    def resize(self):
        self.rect = pygame.Rect(0,0,self.props["width"],self.props["height"])
        self.check_rect = pygame.Rect(0,0,self.props["width"]+(TILE_SIZE_PIXELS*2),self.props["height"]+(TILE_SIZE_PIXELS*2))

    def _check_collision(self, ignore_platforms=False):

        for chunk in self.game.world.grab_all(pix_chunk_range(self.check_rect.topleft, self.check_rect.bottomright)):
            if not chunk:
                return (True, False)
            if not chunk.tiles:
                return (True, False)
            for col_rect, is_platform, tpos in chunk.get_collision():
                if is_platform and ignore_platforms:
                    continue
                if col_rect.colliderect(self.rect):
                    step_up = False
                    if self.step_up and col_rect.bottom in [self.rect.bottom, self.rect.bottom-1, self.rect.bottom+1]:
                        step_up = self.game.world.is_empty((tpos[0], tpos[1]-1), (tpos[0], tpos[1]-1-math.ceil(self.rect.height/TILE_SIZE_PIXELS)))
                    return (col_rect, step_up)
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

        if (col := self._check_collision(True)) and not self.props["noclip"]:
            self.position[0] = prev_x
            self.hugging = True

            if self.step_up and col[1]:
                self.position[1] -= TILE_SIZE_PIXELS+2
                self.position[0] += math.copysign(TILE_SIZE_PIXELS//4, vel_x)

            vel_x = 0
        
        self.position[1] += mov_y
        self.rect.center = self.position
        self.check_rect.center = self.position

        if (col := self._check_collision(vel_y < 0 if not self.ghost_platforms else True)) and not self.props["noclip"]:
            if vel_y > 0:
                self.grounded = True
            self.position[1] = prev_y
            vel_y = 0
            vel_x *= 1 / (1 + (dt * self.props["friction"]))
        else:
            vel_x *= 1 / (1 + (dt * self.props["air_friction"]))

        grav = 0
        if self.props["has_gravity"]:
            grav = TILE_SIZE_PIXELS*dt*2*self.props["mass"]
        else:
            vel_y *= 1 / (1 + (dt * self.props["air_friction"]))

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

    def toggle_noclip(self):
        if not self.props["noclip"]:
            self.change("noclip", True)
            return True
        else:
            self.change("noclip", False)
            return False

    def tick(self):

        pass