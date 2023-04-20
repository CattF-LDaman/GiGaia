from .entity import Entity
from GiGaia.GiCore.Game.Entities.person import Person as PersonBase

import pygame

class Person(Entity, PersonBase):

    def __init__(self, entity_manager, eid, position, props):
        super().__init__(entity_manager, eid, position, props)

        self.is_player = eid == self.game.state.player_eid
        self.rect = pygame.Rect(0,0,40,40)

    def move(self, x, y):
        
        self.em.p.send("CS_MOVE", {"x":x, "y":y})
        self.ghost_position[0] += x*self.game.dt
        self.ghost_position[1] += y*self.game.dt

    @property
    def window_pos(self):  # Position on the actual game window

        if self.is_player:
            return self.game.client.window.get_rect().center
        else:
            return super().window_pos
    
    def draw(self, surf):
        
        self.rect.center = self.draw_pos if not self.is_player else surf.get_rect().center
        pygame.draw.rect(surf, (0,0,255), self.rect, border_radius=self.rect.width//4)