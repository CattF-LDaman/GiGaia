from POA.POAClient.UI.widget import Widget

import pygame

class PageWidget(Widget):

    def __init__(self, ui_manager):

        super().__init__(ui_manager, position=[0.5, 0.5], layer=0, width=0.75, height=0.90, anchor="center", always_redraw=False, head_ui=True)
        
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

        self.surface.fill(self.uim.assets.data.ui.color_B)
        pygame.draw.rect(self.surface, self.uim.assets.data.ui.color_A, self.inner_rect, width=4)
