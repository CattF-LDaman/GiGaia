from GiGaia.GiClient.UI.widget import Widget

import pygame

class PageWidget(Widget):
    """
        A master widget for MainMenu pages
    """

    def __init__(self, ui_manager):

        super().__init__(ui_manager, position=[0.5, 0.5], layer=0, width=0.70, height=0.8, anchor="center", always_redraw=False, head_ui=True)
        
        self.inner_rect = pygame.Rect(0,0,0,0)
        self.inner_rect.width = self.size[0]-10
        self.inner_rect.height = self.size[1]-10
        self.inner_rect.center = self.rect.center

    def handle_resize(self):
        self.inner_rect = pygame.Rect(0,0,0,0)
        self.inner_rect.width = self.size[0]-10
        self.inner_rect.height = self.size[1]-10
        self.inner_rect.center = self.rect.center

    def update(self):

        pass

    def draw(self):

        #self.surface.fill(self.uim.assets.data.ui.color_B)
        #self.surface.fill(self.uim.assets.data.ui.colorkey)
        self.surface.blit(self.uim.assets.page_background, self.rect)
        #pygame.draw.rect(self.surface, self.uim.assets.data.ui.color_A, self.inner_rect, width=4)
        pygame.draw.rect(self.surface, self.uim.assets.data.ui.color_B, self.inner_rect, width=20)
        pygame.draw.rect(self.surface, self.uim.assets.data.ui.color_A, self.inner_rect, width=4)
