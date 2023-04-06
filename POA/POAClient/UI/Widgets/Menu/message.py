
from POA.POAClient.UI.widget import Widget

import pygame

class Message(Widget):

    def __init__(self, ui_manager, pagew, text="", position=(0,0), text_scale=1, color=None):

        super().__init__(ui_manager, position=position, width=0, height=0, relative_to=pagew, anchor="center", relative_anchor="topleft", always_redraw=False)

        self.text = text
        self.text_scale = text_scale
        self.text_color = color if color else self.uim.assets.data.ui.color_tw

        self.adapt_size()

    def adapt_size(self):
        new_size = self.uim.assets.fonts["basic"].get_size2(self.text, self.text_scale)
        self.resize(new_size[0], new_size[1])

    def update(self):

        pass

    def draw(self):

        self.surface.fill(self.uim.assets.data.ui.colorkey)
        self.uim.assets.fonts["basic"].render(self.surface, (0,0) , self.text, scale=self.text_scale, color=pygame.Color(self.text_color))