
from GiGaia.GiClient.UI.widget import Widget
from GiGaia.GiClient.UI.Widgets.text import Message
from GiGaia.GiCore.Game.World.coords import sub_coords,sum_coords

import pygame

class WindowManager:

    def __init__(self, interface):

        self.interface = interface
        self.uim = self.interface.uim
        self.ui = interface.ui

        self.windows = []
    
    def clear(self):
        
        for win in self.windows:
            win.delete()
        self.windows.clear()

    def open_window(self, window, *args, **kwargs):
        for w in self.windows:
            if type(w) == window:
                return
        self.windows.append(self.uim.add_widget(window, wman=self, layer=len(self.windows), *args, **kwargs))


class Window(Widget):

    TITLE = ""

    def __init__(self, ui_manager, wman, size=(0.75,0.90), closable=True, movable=True, layer=0):

        self.wman = wman
        self.interface = wman.interface
        self.ui = wman.ui
        self.game = wman.interface.game
        self.state = self.game.state

        super().__init__(ui_manager, position=[0.5, 0.5], layer=layer, width=size[0], height=size[1], anchor="center", always_redraw=False, relative_to=self.ui, head_ui=True)
        
        self.handle_resize()

        self.uim.add_widget(Message, text=self.TITLE, text_scale=2, shadow=True, font="fat", anchor="midbottom", relative_anchor="midtop", layer=self.layer+1, relative_to=self)

        self.closable = closable
        self.movable = movable

        self.click_start = 0

        self.create()

    def handle_resize(self):
        self.content_rect = pygame.Rect(0,0,0,0)
        self.content_rect.width = self.size[0]
        self.content_rect.height = self.size[1]
        self.content_rect.center = self.rect.center

    def update_windows(self):
        
        raise NotImplementedError

    def create(self):
        
        raise NotImplementedError

    def update(self):

        if self.movable and self.held:
            self.position = sum_coords(self.hold_start, sub_coords(pygame.mouse.get_pos(), self.hold_start))

        if not self == self.wman.windows[-1]:
            for child in self.children:
                child.skip_updates = True
        else:
            for child in self.children:
                child.skip_updates = False
            self.update_window()

    def draw(self):

        #self.surface.fill(self.uim.assets.data.ui.colorkey)
        self.surface.blit(self.uim.assets.window, (0,0))

        pygame.draw.rect(self.surface, self.uim.assets.data.ui.color_B, self.content_rect, width=10)
        pygame.draw.rect(self.surface, self.uim.assets.data.ui.color_A, self.content_rect, width=2)
