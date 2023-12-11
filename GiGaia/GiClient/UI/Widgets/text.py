from GiGaia.GiClient.UI.widget import Widget
from GiGaia.GiCore.color_util import darken

import pygame

class Message(Widget):

    def __init__(self, ui_manager, text="", text_scale=1, font='basic', position=(0,0), anchor="center", relative_anchor="topleft", background_color=None, color=None, shadow=None, shadow_color=None, **kwargs):

        super().__init__(ui_manager, position=position, width=0, height=0, anchor=anchor, relative_anchor=relative_anchor, always_redraw=False, **kwargs)

        self.text = text
        self.text_scale = text_scale
        self.font = font
        self.text_color = color if color else self.uim.assets.data.ui.color_tw
        self.background_color = self.uim.assets.data.ui.colorkey if not background_color else background_color
        self.shadow = shadow
        self.shadow_color = shadow_color

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

        self.surface.fill(self.background_color)

        if self.shadow:
            self.uim.assets.fonts[self.font].render(self.surface, (1,1) , self.text, scale=self.text_scale, color=darken(self.text_color, 20) if not self.shadow_color else self.shadow_color)
        self.uim.assets.fonts[self.font].render(self.surface, (0,0) , self.text, scale=self.text_scale, color=pygame.Color(self.text_color))

class Scrollable(Widget):

    def __init__(self, ui_manager, text="", text_scale=1, font='basic', position=(0,0), anchor="center", relative_anchor="topleft", background_color=None, color=None, scroll_speed=45, **kwargs):

        super().__init__(ui_manager, position=position, width=0, height=0, anchor=anchor, relative_anchor=relative_anchor, always_redraw=False, **kwargs)

        self.text = text
        self.text_scale = text_scale
        self.font = font
        self.text_color = color if color else self.uim.assets.data.ui.color_tw
        self.background_color = self.uim.assets.data.ui.colorkey if not background_color else background_color

        self.scroll = 0
        self.scroll_speed = scroll_speed
        self.auto_scroll = True

        self.scrollbar_width = 3

        self.adapt_size()

    def change(self, text):
        if self.text == text:
            return
        self.text = text
        self.adapt_size()

    @property
    def txt_size(self):
        return self.uim.assets.fonts[self.font].get_size2(self.text, self.text_scale)

    def adapt_size(self):
        self.resize(self.txt_size[0], self.txt_size[1])

    @property
    def scrolled(self):
        return abs(self.scroll/(self.max_scroll))
    
    @property
    def scroll_reach(self): # How much of the text is displayed at one (percentage)
        return self.height/self.txt_size[1]
    
    @property
    def max_scroll(self):
        return -self.txt_size[1]+self.height

    def update(self):

        if self.scrolled_down:
            self.scroll = max(self.scroll-self.scroll_speed, self.max_scroll)
            self.updated = True
            self.auto_scroll = False
        if self.scrolled_up:
            self.scroll = min(self.scroll+self.scroll_speed, 0)
            self.updated = True
            self.auto_scroll = False

        if self.scroll == self.max_scroll:
            self.auto_scroll = True

        if self.auto_scroll:
            self.scroll = self.max_scroll

    def draw(self):

        self.surface.fill(self.background_color)
        self.uim.assets.fonts[self.font].render(self.surface, (0,0+self.scroll) , self.text, scale=self.text_scale, color=pygame.Color(self.text_color))

        if self.txt_size[1] > self.height:
            scrollbar_height = int(self.scroll_reach*self.height/2)
            scrollbar = pygame.Rect(self.width-self.scrollbar_width-1, 1+int((self.height-scrollbar_height-2)*self.scrolled), self.scrollbar_width, scrollbar_height)
            pygame.draw.rect(self.surface, self.uim.assets.data.ui.color_C, scrollbar)


class ScrollableLines(Widget):

    def __init__(self, ui_manager, text="", text_scale=1, line_spacing=3, font='basic', position=(0,0), anchor="center", relative_anchor="topleft", background_color=None, color=None, scroll_speed=1, **kwargs):

        super().__init__(ui_manager, position=position, anchor=anchor, relative_anchor=relative_anchor, always_redraw=False, **kwargs)

        self.lines = text.split("\n") if text else []
        self.text_scale = text_scale
        self.line_spacing = line_spacing
        self.font = font
        self.text_color = color if color else self.uim.assets.data.ui.color_tw
        self.background_color = self.uim.assets.data.ui.colorkey if not background_color else background_color

        self.scroll = 0
        self.scroll_speed = scroll_speed
        self.auto_scroll = True

        self.scrollbar_width = 3

        # self.adapt_size()

    def change(self, text):
        if self.lines == text.split("\n"):
            return
        self.lines = text.split("\n")
        self.updated = True
        # self.adapt_size()

    def add_line(self, text):
        self.lines.extend(text.split("\n"))
        self.updated = True

    @property
    def _font(self):
        return self.uim.assets.fonts[self.font]
    
    # @property
    # def txt_size(self):
    #     return self._font.get_size2(self.text, self.text_scale)

    # def adapt_size(self):
    #     self.resize(self.txt_size[0], self.txt_size[1])

    @property
    def scrolled(self):
        return abs(self.scroll/(self.max_scroll))
    
    @property
    def scroll_reach(self): # How much of the text is displayed at once (percentage)
        # return int(len(self.lines)*self.text_height/self.height)
        return self.height/(self.text_height*len(self.lines))

    @property
    def height_lines(self):  # How many lines can be displayed with current widget height
        return int(self.height/self.line_height)

    @property
    def text_height(self):
        return (self._font.size)*self.text_scale

    @property
    def line_height(self):
        return self.text_height+self.line_spacing

    @property
    def max_scroll(self):
        return max(len(self.lines)-self.height_lines, 0)

    def update(self):

        if self.scrolled_down:
            self.scroll = min(self.scroll+self.scroll_speed, self.max_scroll)
            self.updated = True
            self.auto_scroll = False
        if self.scrolled_up:
            self.scroll = max(self.scroll-self.scroll_speed, 0)
            self.updated = True
            self.auto_scroll = False

        if self.scroll == self.max_scroll:
            self.auto_scroll = True

        if self.auto_scroll:
            self.scroll = self.max_scroll

    def draw(self):

        self.surface.fill(self.background_color)
        for linen, line in enumerate(self.lines[self.scroll: self.scroll+self.height_lines] if len(self.lines) > self.height_lines else self.lines):
            self._font.render(self.surface, (0,0+linen*(self.text_height+self.line_spacing)) , line, scale=self.text_scale, color=pygame.Color(self.text_color))

        if len(self.lines) > self.height_lines:
            scrollbar_height = int(self.scroll_reach*self.height/2)
            scrollbar = pygame.Rect(self.width-self.scrollbar_width-1, 1+int((self.height-scrollbar_height-2)*self.scrolled), self.scrollbar_width, scrollbar_height)
            pygame.draw.rect(self.surface, self.uim.assets.data.ui.color_C, scrollbar)