
from contextlib import redirect_stdout
with redirect_stdout(None):
    import pygame

from GiGaia.GiClient import CLIENT_STATE_INGAME, CLIENT_STATE_MENU
from GiGaia.GiClient.Game.game import Game
from GiGaia.GiClient.MainMenu.menu import Menu
from GiGaia.GiClient.Data.config import DEFAULT_CONFIG
from GiGaia.GiClient.Data.directories import create_directory_structure
from GiGaia.GiClient.Data.Assets import AssetsManager

from GiGaia.GiCore.logging import Logger
from GiGaia.GiCore.config import Config
from GiGaia.GiCore.version import VERSION_STRING
from GiGaia.GiCore.Data import get_data_dir

import GiGaia.GiClient

import os
import sys
import traceback
import time
import shutil

pygame.init()

class Client:

    def __init__(self, location=get_data_dir("GiGaia"), dev=False):

        GiGaia.GiClient.RUNNING_CLIENT = self  # There can only be one... MUAHAHA
        self.dev = dev

        self.session_id = os.urandom(4)
        self.start_time = time.time()

        self.location = location

        self.dirs = create_directory_structure(self.location)

        self.config = Config(self.dirs["configs"], DEFAULT_CONFIG)

        self.log_file_path = os.path.join(self.dirs["logs"], f"GiClient_{int(self.start_time)}_{self.session_id.hex()}.log")

        self.logger = Logger(self.log_file_path, self.config.logging)
        self.log = self.logger.log
        print(f"Logs for current session can be found at ' {self.log_file_path} ''")

        self.log(f"GiGaia with version {VERSION_STRING} (dev={self.dev}) on {sys.platform}")

        if self.dev:
            self.log("Running GiGaia in development mode!", 3)
            shutil.copytree("GiGaia_Assets",self.dirs["assets"], dirs_exist_ok=True)
            self.log("Assets duplicated to data directory.")

        self.window = pygame.display.set_mode((self.config.client.window_width,self.config.client.window_height), pygame.RESIZABLE if not self.config.client.window_fullscreen else pygame.FULLSCREEN)
        pygame.display.set_caption(f"GiGaia {VERSION_STRING}"+(" Development" if self.dev else ""))

        self.clock = pygame.time.Clock()

        self.dt = 0
        self.ticks = 0

        self.state = None
        self.running = False

        self.game = None
        self.menu = None

        self.assets = AssetsManager(self)
        self.assets.load()
        pygame.display.set_icon(self.assets.assets.icon)

        self.log("Client initialized.")

    def run(self):
        try:
            self.running = True
            self.menu = Menu()
            self.state = CLIENT_STATE_MENU
            self.loop()
        except Exception as e:
            self.log(f"Fatal error encountered:\n{''.join(traceback.format_exception(e, value=e ,tb=e.__traceback__))}",5)
            self.close(1)

    def close(self,exit_code=0):

        self.running = False

        if self.game:
            self.game.close()

        if exit_code == 0:
            self.log("Client closed.")
        else:
            self.log(f"Client closed with exit code {exit_code}", 3)

        self.logger.close()

        sys.exit(exit_code)

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                self.close()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_DELETE and pygame.key.get_pressed()[pygame.K_F4]:
                    # Hold F4 and press DEL after to trigger crash
                    raise SystemError("Force crash by user")

            if self.state == CLIENT_STATE_INGAME:
                self.game.handle_event(event)
            elif self.state == CLIENT_STATE_MENU:
                self.menu.handle_event(event)

    def setup_game(self, username, address, port=None):

        if not port:
            port = self.config.networking.default_port

        try:
            self.game = Game((address,port),username)
            return True

        except Exception as e:
            self.log(f"Client encountered an error during game setup:\n{''.join(traceback.format_exception(e, value=e ,tb=e.__traceback__))}",4)
            self.state = CLIENT_STATE_MENU
            return False

    def loop(self):

        while self.running:

            self.dt = self.clock.tick(self.config.client.max_fps)
            self.ticks += self.clock.get_time()

            self.handle_events()
    
            if self.state == CLIENT_STATE_MENU:

                self.menu.tick()

            elif self.state == CLIENT_STATE_INGAME:
                try:
                    self.game.tick()
                except Exception as e:
                    self.log(f"Game encountered an error:\n{''.join(traceback.format_exception(e, value=e ,tb=e.__traceback__))}",4)
                    self.state = CLIENT_STATE_MENU

            pygame.display.flip()