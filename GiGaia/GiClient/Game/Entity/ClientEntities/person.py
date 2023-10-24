from .entity import Entity
from GiGaia.GiCore.Game.Entities.person import Person as PersonBase

import pygame
import math

class Person(Entity, PersonBase):

    def __init__(self, entity_manager, eid, position, props):
        super().__init__(entity_manager, eid, position, props)

        self.is_player = eid == self.game.state.player_eid
        self.rect = pygame.Rect(0,0,30,60)

    def move(self, x):
        
        self.em.p.send("CS_MOVE", {"x":x, "expire":min(int(self.game.dt_ms+self.game.dt_var+(self.game.postman.ping/2)+5), 600)}) # Player keeps moving until 'expire' ms has elapsed
        #self.ghost_position[0] += x*self.game.dt

    def jump(self):

        self.em.p.send("CS_JUMP")
    
    def crouch(self, c):

        self.em.p.send("CS_CROUCH", {"crouching":c})

    def draw(self, surf):

        if self.rect.width != self.props["width"]:
            self.rect.width = self.props["width"]
        if self.rect.height != self.props["height"]:
            self.rect.height = self.props["height"]# - int(4/60*self.props["height"])

        self.rect.center = self.draw_pos
        pygame.draw.rect(surf, (0,0,255), self.rect, border_radius=self.rect.width//4)
        #self.state.lux.point_light(self.draw_pos, 700, (30,30,30))