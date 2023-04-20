
from GiGaia.GiClient.Networking.connect import connect, login
from GiGaia.GiClient.Networking.postman import Postman
from GiGaia.GiClient import CLIENT_STATE_MENU, CLIENT_STATE_INGAME

from GiGaia.GiClient.Game.States import STATES

from GiGaia.GiClient.UI.ui_manager import UIManager
from GiGaia.GiClient.UI.Widgets.debugpanel import DebugPanel
from GiGaia.GiClient.UI.Widgets.devindicator import DevIndicator
from GiGaia.GiClient.UI.Widgets.quitdialog import QuitDialog
from GiGaia.GiClient.UI.Widgets.text import Message

from GiGaia.GiCore.Networking.Packets import PID

import pygame

class Game:

    def __init__(self, addr, username):
        
        from GiGaia.GiClient import RUNNING_CLIENT
        self.client = RUNNING_CLIENT

        self.config = self.client.config

        self.scale = self.config.client.game_scale
        self.resize()
        
        self.keybinds = self.client.keybinds
        self.assets = self.client.assets

        self.username = username
        self.addr = addr

        self.debug = False
        self.fps_counter = False
        self.closed = False
        self.quit_dialog = None

        self.state = None

    def resize(self):

        scr = self.client.window.get_size()
        self.screen = pygame.Surface((int(scr[0]/self.scale), int(scr[1]/self.scale)))

    def handle_event(self, event):

        self.ui_manager.handle_event(event)

        if self.state:
            self.state.handle_event_master(event)

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

                case pygame.K_F3:
                    if not self.fps_counter:
                        self.fps_counter = self.uim.add_widget(Message, text="", anchor="topleft", position=(4,4), text_scale=2, color=(255,255,255))
                    else:
                        self.fps_counter.delete()
                        self.fps_counter = None
                case pygame.K_F2:
                    if self.quit_dialog and not self.quit_dialog.deleted:
                        self.quit_dialog.delete()
                        self.quit_dialog = None
                    else:
                        self.quit_dialog = self.uim.add_widget(QuitDialog)

    def establish_connection(self):

        self.conn = connect(self.addr)
        if isinstance(self.conn, Exception):
            self.client.log(f"Unable to connect to {self.addr[0]}:{self.addr[1]}",4)
            raise self.conn

        login(self.conn, self.username)


    def start(self):  # Most initialisation of networking and game should go here.

        self.establish_connection()
        
        self.postman = Postman(self)
        self.postman.hold(PID.SC_LOAD_STATE)
        self.postman.start()

        self.ui_manager = self.uim = UIManager(self.client)
        if self.client.dev:
            self.ui_manager.add_widget(DevIndicator)

        self.client.state = CLIENT_STATE_INGAME

    def handle_state(self):

        ssp = self.postman.fetch(PID.SC_LOAD_STATE)
        if ssp:
            if self.state:
                self.state.destroy_master()

            s = ssp[-1]
            self.state = STATES[s.sid](self)
            self.state.setup_master()

        if self.state:
            self.state.tick()

    def tick(self):

        self.dt = self.client.dt

        self.screen.fill((25,25,25))
        if self.fps_counter:
            self.fps_counter.change(str(int(self.client.clock.get_fps())))

        self.handle_state()

        self.show() # Displays everything in the game world

        self.ui_manager.update(self.client.ticks) # Handles everything UI including drawing

    def show(self):

        if self.scale > 1:
            self.client.window.blit(pygame.transform.scale(self.screen, self.client.window.get_size()), (0,0))
        else:
            self.client.window.blit(self.screen, (0,0))

    def close(self):
        if not self.closed:
            self.closed = True
            self.postman.close()
            self.client.game = None
            self.client.state = CLIENT_STATE_MENU