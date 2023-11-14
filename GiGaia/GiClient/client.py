
import pygame
from pygame._sdl2 import messagebox

from GiGaia.GiClient import CLIENT_STATE_INGAME, CLIENT_STATE_MENU
from GiGaia.GiClient.Game.game import Game
from GiGaia.GiClient.MainMenu.menu import Menu
from GiGaia.GiClient.Data.config import DEFAULT_CONFIG
from GiGaia.GiClient.Data.keybinds import Keybinds
from GiGaia.GiClient.Data.directories import create_directory_structure

from GiGaia.GiCore.Data.Assets import AssetsManager
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

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

class Client:

    def __init__(self, location=get_data_dir("GiGaia"), dev=False):

        GiGaia.GiClient.RUNNING_CLIENT = self  # There can only be one... MUAHAHA
        self.dev = dev

        self.session_id = os.urandom(4)  # A four-byte sequence used to help identify the current instance of the game
        self.start_time = time.time()

        self.location = location  # Will run from this location, all data like logs, configs, etc. will be found in this directory

        self.dirs = create_directory_structure(self.location)  # Dictionary containing the location of data directories eg. self.dirs['logs']

        self.config = Config(self.dirs["configs"], DEFAULT_CONFIG)

        self.log_file_path = os.path.join(self.dirs["logs"], f"GiClient_{int(self.start_time)}_{self.session_id.hex()}.log")

        self.logger = Logger(self.log_file_path, self.config.logging)
        self.log = self.logger.log
        print(f"Logs for current session can be found at ' {self.log_file_path} ''")

        self.log(f"GiGaia with version {VERSION_STRING} (dev={self.dev}) on {sys.platform}")

        if self.dev:
            self.log("Running GiGaia in development mode!", 3)
            shutil.copytree("GiGaia_Assets",self.dirs["assets"], dirs_exist_ok=True)  # Copies the current assets from dev environment to data dir
            self.log("Assets duplicated to data directory.")

        self.window = pygame.display.set_mode((self.config.client.window_width,self.config.client.window_height), pygame.RESIZABLE if not self.config.client.window_fullscreen else pygame.FULLSCREEN)
        pygame.display.set_caption(f"GiGaia {VERSION_STRING}"+(" Development" if self.dev else ""))

        self.clock = pygame.time.Clock()

        self.dt = 0  # Deltatime in seconds (frame time)
        self.dt_ms = 0  # Deltatime in ms
        self.dt_var = 0  # Difference between frame times of two last ticks
        self.ticks = 0  # Ticks isn't actually the number of ticks, but the total number of ms that has passed

        self.state = None  # A constant, defines what to do every frame. (Main menu or in-game) GiGaia.GiClient: CLIENT_STATE_INGAME, CLIENT_STATE_MENU
        self.running = False

        self.game = None  # The game object, gets created when joining in 'self.setup_game'
        self.menu = None  # Main menu object, created in 'self.run'

        self.assets = AssetsManager(self) # Handles assets, obviously
        self.assets.load()
        pygame.display.set_icon(self.assets.assets.icon)

        self.keybinds = Keybinds(self.location)  # Keybinds datafile, loaded from data dir

        self.log("Client initialized.")

    def run(self):
        try:
            self.running = True
            self.menu = Menu()
            self.state = CLIENT_STATE_MENU
            self.loop()
        except Exception as e:
            self.log(err_msg := f"Fatal error encountered:\n{''.join(traceback.format_exception(e, value=e ,tb=e.__traceback__))}",5)
            messagebox("Crashed!", err_msg+f'\n{self.log_file_path}', error=True)
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

            if event.type == pygame.WINDOWRESIZED:
                if self.state == CLIENT_STATE_INGAME:
                    self.game.resize()

            if event.type == pygame.KEYDOWN:

                if self.dev and event.key == pygame.K_DELETE and pygame.key.get_pressed()[pygame.K_F4]:
                    # Hold F4 and press DEL after to trigger crash
                    raise SystemError("Force crash by user")
                
                elif event.key == pygame.K_F3 and self.dev:

                    self.log(f"{self.clock.get_fps()} FPS")

                elif event.key == pygame.K_F12:
                    
                    pygame.image.save(self.window, os.path.join(self.dirs["screenshots"], f"scr_{self.session_id.hex()}{int(time.time())}.png"))
                    self.log("Screenshot taken.")

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
            self.menu.lost_connection = f"Game setup error: {e}"
            return False

    def loop(self):

        while self.running:
            
            self._prev_dt_ms = self.dt_ms
            self.dt_ms = self.clock.tick(self.config.client.max_fps)
            self.dt_var = abs(self.dt_ms - self._prev_dt_ms)
            self.dt = self.dt_ms/1000
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
                    self.menu.lost_connection = f"Game error: {''.join(traceback.format_exception(e, value=e ,tb=e.__traceback__)) if self.dev else self.log_file_path}"

            pygame.display.flip()