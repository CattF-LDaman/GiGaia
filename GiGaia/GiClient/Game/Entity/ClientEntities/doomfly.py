
from .entity import Entity
from GiGaia.GiCore.Game.Entities import Doomfly as DoomflyBase

import pygame

class Doomfly(Entity, DoomflyBase):

    def __init__(self, entity_manager, eid, position, props):
        super().__init__(entity_manager, eid, position, props)

        self.rect = pygame.Rect(0,0,2,2)

    def draw(self, surf):

        self.rect.center = self.draw_pos
        pygame.draw.rect(surf, self.props["color"], self.rect, border_radius=self.rect.width//3)

        if not self.props["resting"]:
            self.state.lux.point_light(self.draw_pos, 6, (255,40,40))
            self.state.lux.point_light(self.draw_pos, 10, (255,40,40))
            pygame.draw.rect(self.state.lux.lit_up_surface, (255,40,40), self.rect)