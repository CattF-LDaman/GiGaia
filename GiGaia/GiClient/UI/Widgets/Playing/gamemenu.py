from GiGaia.GiClient.UI.widget import Widget

from GiGaia.GiClient.UI.Widgets.button import ActionButton
from GiGaia.GiClient.UI.Widgets.text import Message

import pygame

class GameMenu(Widget):

    def __init__(self, ui_manager, game):

        super().__init__(ui_manager, position=[0, 0], layer=30, width=400, height=1.0, anchor="topleft", always_redraw=False, head_ui=True)
        
        self.inner_rect = pygame.Rect(0,0,0,0)
        self.inner_rect.width = self.size[0]-10
        self.inner_rect.height = self.size[1]-10
        self.inner_rect.center = self.rect.center

        self.uim.add_widget(Message, text="GiGaia", position=[0, 0.04], text_scale=2, shadow=True, shadow_color=(31, 96, 64), color=ui_manager.assets.data.ui.color_txt, font="fat", anchor="center", relative_anchor="midtop", layer=31, relative_to=self)
        self.uim.add_widget(ActionButton, text="Continue", width=0.9, height=50, action=self.delete, position=[0, 0.1], anchor="center", relative_anchor="midtop", relative_to=self, layer=31)
        self.uim.add_widget(ActionButton, text="Quit", width=0.9, height=50, action=game.close, position=[0, 0.2], anchor="center", relative_anchor="midtop", relative_to=self, layer=31)

    def handle_resize(self):
        self.inner_rect = pygame.Rect(0,0,0,0)
        self.inner_rect.width = self.size[0]-10
        self.inner_rect.height = self.size[1]-10
        self.inner_rect.center = self.rect.center

    def update(self):

        pass

    def draw(self):

        self.surface.blit(self.uim.assets.page_background, self.rect)
        pygame.draw.rect(self.surface, self.uim.assets.data.ui.color_B, self.inner_rect, width=20)
        pygame.draw.rect(self.surface, self.uim.assets.data.ui.color_A, self.inner_rect, width=4)

