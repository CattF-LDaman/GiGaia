
from POA.POAClient.UI.widget import Widget

import pygame

class GameTitle(Widget):

    def __init__(self, ui_manager, pagew):

        super().__init__(ui_manager, position=[0, 0.05], width=4*8*max(len(w) for w in "Plan Of Action".split('\n')), height=400, relative_to=pagew, anchor="midtop", relative_anchor="midtop", always_redraw=False)

    def update(self):

        pass

    def draw(self):

        self.surface.fill(self.uim.assets.data.ui.colorkey)
        self.uim.assets.fonts["basic"].render(self.surface, (0,0) , "Plan of Action", scale=4, color=pygame.Color(self.uim.assets.data.ui.color_txt))

class Title(Widget):

    def __init__(self, ui_manager, pagew, text):

        self.text = text
        super().__init__(ui_manager, position=[0, 0.05], width=4*8*max(len(w) for w in text.split('\n')), height=400, relative_to=pagew, anchor="midtop", relative_anchor="midtop", always_redraw=False)

    def update(self):

        pass

    def draw(self):

        self.surface.fill(self.uim.assets.data.ui.colorkey)
        self.uim.assets.fonts["basic"].render(self.surface, (0,0) , self.text, scale=4, color=pygame.Color(self.uim.assets.data.ui.color_txt))