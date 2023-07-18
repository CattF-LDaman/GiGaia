
from .entity import Entity
from GiGaia.GiCore.Game.Entities.blob import Blob as BlobBase

import pygame

class Blob(Entity, BlobBase):

    def __init__(self, entity_manager, eid, position, props):
        super().__init__(entity_manager, eid, position, props)

        self.rect = pygame.Rect(0,0,32,16)

    def draw(self, surf):

        self.rect.center = self.draw_pos
        pygame.draw.rect(surf, (80,250,80), self.rect, border_radius=self.rect.width//4)