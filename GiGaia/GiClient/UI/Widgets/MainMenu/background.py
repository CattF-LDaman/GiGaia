from GiGaia.GiClient.UI.widget import Widget

import pygame

class Background(Widget):

    def __init__(self, ui_manager):

        super().__init__(ui_manager, position=[0.5, 0.5], layer=0, width=1.0, height=1.0, anchor="center", always_redraw=False, head_ui=False)
        
        self.bg_sprite = self.uim.assets.background
        self.bg_rect = self.bg_sprite.get_rect()
        self.bg_rect.center = self.rect.center

    def handle_resize(self):
        self.bg_rect.center = self.rect.center

    def update(self):

        pass

    def draw(self):

        #self.surface.fill(self.uim.assets.data.ui.color_B)
        #pygame.draw.rect(self.surface, self.uim.assets.data.ui.color_A, self.inner_rect, width=4)

        self.surface.blit(self.bg_sprite, self.bg_rect)
