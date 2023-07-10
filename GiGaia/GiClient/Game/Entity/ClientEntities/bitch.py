
from .entity import Entity
from GiGaia.GiCore.Game.Entities import Bitch as BitchBase

import pygame

class Bitch(Entity, BitchBase):

    def __init__(self, entity_manager, eid, position, props):
        super().__init__(entity_manager, eid, position, props)

        self.rect = pygame.Rect(0,0,2,2)

    def draw(self, surf):

        self.rect.center = self.draw_pos
        pygame.draw.rect(surf, self.props["color"], self.rect, border_radius=self.rect.width//3)

        self.state.lux.point_light(self.draw_pos, 6, (40,255,40))
        self.state.lux.point_light(self.draw_pos, 10, (40,255,40))