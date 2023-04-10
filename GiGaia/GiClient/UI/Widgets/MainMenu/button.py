from GiGaia.GiClient.UI.widget import Widget

import pygame
import math

class PageLink(Widget):

    def __init__(self, ui_manager, pagew, pos, text, menu, page_to):

        super().__init__(ui_manager, position=[0, pos], width=0.4, layer=3, height=80, anchor="center", relative_anchor="midtop", relative_to=pagew, always_redraw=False)

        self.color = pygame.Color(self.uim.assets.data.ui.color_B)
        self.text = text
        
        self.menu = menu
        self.page_to = page_to

    def update(self):
        if self.clicked:
            self.uim.assets.sounds["click"].play()
            self.menu.switch(self.page_to)

        if self.hovered_once:
            self.uim.assets.sounds["hover"].play()

        self.updated = self.updated or self.hovered_once or self.unhovered

    def draw(self):

        if not self.hovered:
            self.surface.fill(self.color)
            pygame.draw.rect(self.surface, self.uim.assets.data.ui.color_A, self.rect, width=5)
        else:
            self.surface.fill(self.uim.assets.data.ui.color_A)
            pygame.draw.rect(self.surface, self.uim.assets.data.ui.color_C, self.rect, width=5)
        self.uim.assets.fonts["basic"].render(self.surface, self.rect.center, self.text, blit_anchor_center=True, scale=3, color=pygame.Color(self.uim.assets.data.ui.color_txt))

class BackButton(Widget):

    def __init__(self, ui_manager, pagew, back):

        super().__init__(ui_manager, position=[0, 0], width=0.1, layer=3, height=40, anchor="center", relative_anchor="topleft", relative_to=pagew, always_redraw=False)

        self.color = pygame.Color(self.uim.assets.data.ui.color_B)
        self.text = "X"
        
        self.back = back

    def update(self):
        if self.clicked:
            self.uim.assets.sounds["click"].play()
            self.back()

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
        self.uim.assets.fonts["basic"].render(self.surface, self.rect.center, self.text, blit_anchor_center=True, scale=4, color=pygame.Color(self.uim.assets.data.ui.color_txt))

class ActionButton(Widget):

    def __init__(self, ui_manager, pagew, text, action, position=(0,0), width=0.4, height=80, text_color=None):

        super().__init__(ui_manager, position=position, width=width, layer=3, height=height, anchor="center", relative_anchor="topleft", relative_to=pagew, always_redraw=False)

        self.color = pygame.Color(self.uim.assets.data.ui.color_B)
        self.text_color = pygame.Color(self.uim.assets.data.ui.color_txt) if not text_color else pygame.Color(text_color)
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
        self.uim.assets.fonts["basic"].render(self.surface, self.rect.center, self.text, blit_anchor_center=True, scale=4, color=self.text_color)
