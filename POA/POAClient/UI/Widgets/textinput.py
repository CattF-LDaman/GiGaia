
from POA.POAClient.UI.widget import Widget

import pygame
import re

class RawInput(Widget):

    def __init__(self, ui_manager, size, font="basic", name="Input", default="", allowed_chars=None, text_scale=1, typing_char="|", *args, **kwargs):

        self.name = name

        self.input_size = size
        self.font = ui_manager.assets.fonts[font]

        super().__init__(ui_manager, *args, width=self.font.get_size(self.input_size+1, text_scale)+2, height=10*text_scale, always_redraw=True, **kwargs)#position=[0.5, 0.5], width=600, height=200, anchor="center", always_redraw=True)
        
        self.allowed_chars = allowed_chars
        if allowed_chars:
            self._ac_regex = f"[^{allowed_chars}]"

        self.text_scale = text_scale
        self.typing_char = typing_char

        self.text_input = default
        self.prev_input = self.text_input

    def update(self):
        
        if self.clicked and not self.capturing:
            self.ui_manager.capture_input(self)

        elif self.unclicked and self.capturing:
            self.ui_manager.stop_capturing_input(self)

        if self.prev_input != self.text_input:
            if self.allowed_chars:
                self.text_input = re.sub(self._ac_regex, '', self.text_input)
            self.text_input = self.text_input[:self.input_size]
            self.updated = True
            self.prev_input = self.text_input

        self.content = self.text_input

    def draw(self):

        self.surface.fill(self.uim.assets.data.ui.colorkey)

        inp_content = self.content
        if self.capturing and (self.age//600) % 2 == 0:
            inp_content += self.typing_char

        self.uim.assets.fonts["basic"].render(self.surface, (2,2) , inp_content, multiline=False, scale=self.text_scale)

class InputLabel(Widget):

    def __init__(self, ui_manager, text, linput):

        super().__init__(ui_manager, position=[0, -2], layer=1, width=linput.font.get_size(text, linput.text_scale), height=8*linput.text_scale, relative_to=linput, anchor="bottomleft", relative_anchor="topleft", always_redraw=False)
        self.text = text
        self.linput = linput

    def update(self):

        pass

    def draw(self):

        self.surface.fill(self.uim.assets.data.ui.colorkey)
        self.uim.assets.fonts["basic"].render(self.surface, (0,0) , self.text, scale=self.linput.text_scale, color=pygame.Color(self.uim.assets.data.ui.color_A))

class Input(RawInput):

    def __init__(self, ui_manager, *args, isize_w=None, isize_h=None, placeholder="", **kwargs):

        super().__init__(ui_manager, *args, **kwargs)

        tsize = self.font.get_size2(self.input_size+1, self.text_scale)
        self.resize(w=tsize[0]+4 if not isize_w else isize_w, h=tsize[1] if not isize_h else isize_h)

        if self.name:
            self.uim.add_widget(InputLabel, self.name, self)

        self.color = pygame.Color(self.uim.assets.data.ui.color_B)
        self.placeholder = placeholder

    def draw(self):

        if not self.hovered:
            self.surface.fill(self.color)
            pygame.draw.rect(self.surface, self.uim.assets.data.ui.color_A, self.rect, width=5)
        else:
            self.surface.fill(self.uim.assets.data.ui.color_A)
            pygame.draw.rect(self.surface, self.uim.assets.data.ui.color_C, self.rect, width=5)

        inp_content = self.content
        if self.capturing and (self.age//600) % 2 == 0:
            inp_content += self.typing_char

        if not self.capturing and not inp_content and self.placeholder:
            self.font.render(self.surface, (2,4*self.text_scale) , self.placeholder, scale=self.text_scale, multiline=False, color=pygame.Color(self.uim.assets.data.ui.color_tg))
        else:
            self.font.render(self.surface, (2,4*self.text_scale) , inp_content, scale=self.text_scale, multiline=False, color=pygame.Color(self.uim.assets.data.ui.color_txt))
