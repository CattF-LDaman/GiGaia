from POA.POAClient.UI.widget import Widget

import pygame

class ActionButton(Widget):

    def __init__(self, ui_manager, text, action, text_color=None, text_scale=4, font="basic", position=(0,0), width=0.4, height=80, anchor='center', relative_anchor='topleft', **kwargs):

        super().__init__(ui_manager, position=position, width=width, height=height, relative_anchor=relative_anchor, anchor=anchor, **kwargs)

        self.color = pygame.Color(self.uim.assets.data.ui.color_B)
        self.text_color = pygame.Color(self.uim.assets.data.ui.color_txt) if not text_color else pygame.Color(text_color)
        self.text_scale = text_scale
        self.font = font
        self.text = text
        
        self.action = action

    def update(self):
        if self.clicked:
            self.uim.assets.sounds["click"].play()
            self.action()

        if self.hovered_once:
            self.uim.assets.sounds["hover"].play()

        self.updated = self.updated or self.hovered or self.unhovered

    def draw(self):

        if not self.hovered:
            self.surface.fill(self.color)
            pygame.draw.rect(self.surface, self.uim.assets.data.ui.color_A, self.rect, width=5)
        else:
            self.surface.fill(self.uim.assets.data.ui.color_A)
            pygame.draw.rect(self.surface, self.uim.assets.data.ui.color_C, self.rect, width=5)
        self.uim.assets.fonts[self.font].render(self.surface, self.rect.center, self.text, blit_anchor_center=True, scale=self.text_scale, color=self.text_color)
