
from .entity import Entity
from GiGaia.GiCore.Game.Entities.boink import Boink as BoinkBase

import pygame

class Boink(Entity, BoinkBase):

    def __init__(self, entity_manager, eid, position, props):
        super().__init__(entity_manager, eid, position, props)

        self.rect = pygame.Rect(0,0,12,12)

    def draw(self, surf):

        self.rect.center = self.draw_pos
        pygame.draw.rect(surf, (70,70,255), self.rect, border_radius=2)