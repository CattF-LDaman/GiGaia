
from GiGaia.GiClient.Game.interface import Interface

from GiGaia.GiClient.Game.Interfaces.PlayingUI.windows import WindowManager
from GiGaia.GiClient.Game.Interfaces.PlayingUI.chat import Chat
from GiGaia.GiClient.Game.Interfaces.PlayingUI.inventory import Inventory
from GiGaia.GiClient.Game.Interfaces.PlayingUI.structurizer import Structurizer

from GiGaia.GiClient.UI.Widgets.text import Message
from GiGaia.GiClient.UI.Widgets.Playing.entityname import EntityName
from GiGaia.GiClient.UI.Widgets.Playing.gamemenu import GameMenu

from GiGaia.GiCore.Game.World.coords import div_coord, TILE_SIZE_PIXELS

import pygame

class Playing(Interface):

    def __init__(self, state):
        super().__init__(state)

        self.game_menu = None

        self.wman = WindowManager(self)

        self.player_names = {}

        self.structurizer_points = [None, None]
        self.structurizer_core = None

    def handle_event(self, event):

        pressed = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:

            match event.key:

                case pygame.K_ESCAPE:
                    if self.wman.windows:
                        self.wman.windows[-1].delete()
                        self.wman.windows.pop(-1)
                    elif not self.chat.hidden:
                        self.chat.hide()
                    elif self.game_menu and not self.game_menu.deleted:
                        self.game_menu.delete()
                        self.game_menu = None
                    else:
                        self.game_menu = self.uim.add_widget(GameMenu, self.game)

                case self.state.keybinds.CHAT:
                    if self.chat.hidden:
                        self.chat.reveal()

                case self.state.keybinds.CHAT_SEND:
                    if self.chat.typing:
                        self.chat.send()
                    else:
                        self.chat.chat_input.start_input()
                
                case self.state.keybinds.CHAT_HUP if not self.chat.hidden:
                    self.chat.history_select()
                    
                case self.state.keybinds.CHAT_HDOWN if not self.chat.hidden:
                    self.chat.history_select(-1)

                case self.state.keybinds.INVENTORY if self.chat.hidden and not self.wman.windows:
                    self.open_window(Inventory)

                case self.state.keybinds.STRUCTURIZER if self.chat.hidden:
                    if pressed[pygame.K_PAGEUP]:
                        if not self.structurizer_points[0]:
                            self.set_structurizer_point(0)
                        elif not self.structurizer_points[1]:
                            self.set_structurizer_point(1)
                        else:
                            self.structurizer_points = [None, None]
                    elif pressed[pygame.K_HOME]:
                        self.set_structurizer_core()
                    else:
                        self.open_window(Structurizer)

    def set_structurizer_point(self, index):
        def most_topleft_point(point1, point2):
            x1, y1 = point1
            x2, y2 = point2
            if x1 < x2:
                return point1
            elif x1 > x2:
                return point2
            else:
                if y1 < y2:
                    return point1
                else:
                    return point2
        
        tpos_m = div_coord(self.state.scene.mouse, TILE_SIZE_PIXELS, floor=True)
        self.structurizer_points[index] = tpos_m
        if all(self.structurizer_points) and self.structurizer_points[0] != most_topleft_point(*self.structurizer_points):
            self.structurizer_points[0], self.structurizer_points[1] = self.structurizer_points[1], self.structurizer_points[0]

    def set_structurizer_core(self):

        tpos_m = div_coord(self.state.scene.mouse, TILE_SIZE_PIXELS, floor=True)
        self.structurizer_core = tpos_m

    def open_window(self, window, *args, **kwargs):
        self.wman.open_window(window, *args, **kwargs)

    def create(self):

        self.chat = self.uim.add_widget(Chat, self)
        self.chat.hide()
        
        #self.uim.add_widget(Message, text="GiGaia", text_scale=10, position=[0, 0], anchor="center", relative_anchor="center", relative_to=self.ui, skip_event=True)

    def entity_name(self, ent):

        self.uim.add_widget(EntityName, entity=ent, ui_frame=self.ui)
