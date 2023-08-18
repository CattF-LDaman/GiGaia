
from .entity import Entity
from GiGaia.GiCore.Game.Entities import ItemEntity as ItemEntityBase

import pygame

class ItemEntity(Entity, ItemEntityBase):

    def __init__(self, entity_manager, eid, position, props):
        super().__init__(entity_manager, eid, position, props)

        self.rect = pygame.Rect(0,0,9,9)

    def draw(self, surf):

        self.rect.center = self.draw_pos
        pygame.draw.rect(surf, (80,80,80), self.rect, border_radius=self.rect.width//4)