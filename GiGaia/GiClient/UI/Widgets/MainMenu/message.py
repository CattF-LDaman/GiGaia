
from GiGaia.GiClient.UI.widget import Widget

from GiGaia.GiCore.Game.World.coords import add_coord
from GiGaia.GiCore.color_util import darken

import pygame

class Message(Widget):

    def __init__(self, ui_manager, pagew, text="", position=(0,0), text_scale=1, color=None, shadow=None, shadow_color=None, font="basic"):

        super().__init__(ui_manager, position=position, width=0, height=0, relative_to=pagew, anchor="center", relative_anchor="topleft", always_redraw=False)

        self.text = text
        self.text_scale = text_scale
        self.text_color = color if color else self.uim.assets.data.ui.color_tw

        self.shadow = shadow
        self.shadow_color = shadow_color

        self.font = font

        self.adapt_size()

    def adapt_size(self):
        new_size = self.uim.assets.fonts[self.font].get_size2(self.text, self.text_scale)
        if self.shadow:
            new_size = add_coord(new_size, 1)
        self.resize(new_size[0], new_size[1])

    def update(self):

        pass

    def draw(self):

        self.surface.fill(self.uim.assets.data.ui.colorkey)
        if self.shadow:
            self.uim.assets.fonts[self.font].render(self.surface, (1,1) , self.text, scale=self.text_scale, color=darken(self.text_color, 20) if not self.shadow_color else self.shadow_color)
        self.uim.assets.fonts[self.font].render(self.surface, (0,0) , self.text, scale=self.text_scale, color=pygame.Color(self.text_color))