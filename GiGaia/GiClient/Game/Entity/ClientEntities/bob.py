
from .entity import Entity
from GiGaia.GiCore.Game.Entities.bob import Bob as BobBase

import pygame

class Bob(Entity, BobBase):

    def __init__(self, entity_manager, eid, position, props):
        super().__init__(entity_manager, eid, position, props)

        self.rect = pygame.Rect(0,0,50,50)

    def draw(self, surf):

        self.rect.center = self.draw_pos
        pygame.draw.rect(surf, (255,0,0), self.rect, border_radius=self.rect.width//2)