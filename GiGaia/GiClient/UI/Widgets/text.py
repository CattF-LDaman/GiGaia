from GiGaia.GiClient.UI.widget import Widget

import pygame

class Message(Widget):

    def __init__(self, ui_manager, text="", text_scale=1, font='basic', position=(0,0), anchor="center", relative_anchor="topleft", color=None, **kwargs):

        super().__init__(ui_manager, position=position, width=0, height=0, anchor=anchor, relative_anchor=relative_anchor, always_redraw=False, **kwargs)

        self.text = text
        self.text_scale = text_scale
        self.font = font
        self.text_color = color if color else self.uim.assets.data.ui.color_tw

        self.adapt_size()

    def change(self, text):
        if self.text == text:
            return
        self.text = text
        self.adapt_size()

    def adapt_size(self):
        new_size = self.uim.assets.fonts[self.font].get_size2(self.text, self.text_scale)
        self.resize(new_size[0], new_size[1])

    def update(self):

        pass

    def draw(self):

        self.surface.fill(self.uim.assets.data.ui.colorkey)
        self.uim.assets.fonts[self.font].render(self.surface, (0,0) , self.text, scale=self.text_scale, color=pygame.Color(self.text_color))