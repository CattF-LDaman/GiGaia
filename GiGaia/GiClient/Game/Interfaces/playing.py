
from GiGaia.GiClient.Game.interface import Interface

from GiGaia.GiClient.Game.Interfaces.PlayingUI.windows import WindowManager
from GiGaia.GiClient.Game.Interfaces.PlayingUI.chat import Chat

from GiGaia.GiClient.UI.Widgets.text import Message
from GiGaia.GiClient.UI.Widgets.Playing.entityname import EntityName
from GiGaia.GiClient.UI.Widgets.Playing.gamemenu import GameMenu

import pygame

class Playing(Interface):

    def __init__(self, state):
        super().__init__(state)

        self.game_menu = None

        self.wman = WindowManager(self)

        self.player_names = {}

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            match event.key:

                case pygame.K_ESCAPE:
                    if self.wman.windows:
                        self.wman.windows[-1].delete()
                        self.wman.windows.pop(-1)
                    elif not self.chat.hidden:
                        self.chat.hide()
                    elif self.game_menu:
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

    def open_window(self, window, *args, **kwargs):
        self.wman.open_window(window, *args, **kwargs)

    def create(self):

        self.chat = self.uim.add_widget(Chat, self)
        self.chat.hide()
        #self.uim.add_widget(Message, text="GiGaia", text_scale=10, position=[0, 0], anchor="center", relative_anchor="center", relative_to=self.ui, skip_event=True)

    def entity_name(self, ent):

        self.uim.add_widget(EntityName, entity=ent, ui_frame=self.ui)
