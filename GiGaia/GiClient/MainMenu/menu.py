
from GiGaia.GiClient import CLIENT_STATE_MENU, CLIENT_STATE_INGAME

from GiGaia.GiClient.UI.ui_manager import UIManager
from GiGaia.GiClient.UI.Widgets.devindicator import DevIndicator
from GiGaia.GiClient.UI.Widgets.debugpanel import DebugPanel

from GiGaia.GiClient.MainMenu.MenuPages import PAGES

from GiGaia.GiCore.threading import threaded_daemon

import pygame
import traceback

from getpass import getuser
import time

class Menu:

    def __init__(self):
        
        from GiGaia.GiClient import RUNNING_CLIENT
        self.client = RUNNING_CLIENT

        self.config = self.client.config

        self.screen = self.client.window #pygame.Surface((self.config.client.window_width, self.config.client.window_height))

        self.debug = False

        self.ui_manager = self.uim = UIManager(self.client)
        if self.client.dev:
            self.ui_manager.add_widget(DevIndicator)

        self.page = None

        self.join_status = None
        self.join_failed = False

        self.switch('Start')

    def switch(self, page):

        if self.page:
            self.page.destroy()

        self.page = PAGES[page](self)
        self.page.create()

    @threaded_daemon
    def join(self, addr, username):
        
        gm_succ = self.client.setup_game(username, addr[0], addr[1])
        if not gm_succ:
            self.join_status = "Error creating game object (check logs)"
            self.join_failed = True
            return

        try:
            self.client.game.start()
            self.switch("Start")
        except Exception as e:
            self.client.log("Unable to join: " + ''.join(traceback.format_exception(e, value=e ,tb=e.__traceback__)), 4)
            self.join_status = type(e).__name__
            self.join_failed = True
            return
    
    def start_join(self, addr, username):

        self.join_status = "Joining..."
        self.switch('Joining')
        self.join(addr, username)
        

    def handle_event(self, event):

        self.ui_manager.handle_event(event)
        
        if event.type == pygame.KEYDOWN:
            match event.key:

                case pygame.K_F8 if self.client.dev:
                    if not self.debug:
                        self.client.logger.print_all = True
                        self.client.log("Debug mode enabled.")
                        self.debug = self.uim.add_widget(DebugPanel)
                    else:
                        self.client.logger.print_all = False
                        self.debug.delete()
                        self.debug = False

                case pygame.K_F1 if self.client.dev:
                    self.start_join(("localhost", 17746), f"dev{getuser().encode('utf-8').hex()[:3]}")

                case pygame.K_RETURN:
                    self.page.enter()

                case pygame.K_ESCAPE:
                    self.page.back()

    def tick(self):
        
        self.draw()

        self.ui_manager.update(self.client.ticks) # Handles everything UI including drawing
        self.page.update()

    def draw(self):
        
        self.screen.fill((25,25,25))

