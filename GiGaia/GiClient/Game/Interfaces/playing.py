
from GiGaia.GiClient.Game.interface import Interface

from GiGaia.GiClient.UI.Widgets.panel import Panel
from GiGaia.GiClient.UI.Widgets.text import Message
from GiGaia.GiClient.UI.Widgets.Playing.gamemenu import GameMenu

import pygame

class Playing(Interface):

    def __init__(self, state):
        super().__init__(state)

        self.game_menu = None

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            match event.key:

                case pygame.K_ESCAPE:
                    if self.game_menu:
                        self.game_menu.delete()
                        self.game_menu = None
                    else:
                        self.game_menu = self.uim.add_widget(GameMenu, self.game)

    def create(self):

        self.uim.add_widget(Message, text="GiGaia", text_scale=10, position=[0, 0], anchor="center", relative_anchor="center")
