
import os
import json
from types import SimpleNamespace

from GiGaia.GiCore.Networking import DEFAULT_SERVER_PORT
from GiGaia.GiCore.Game.World.Generation.Layers import SETTINGS


class Config:

    __DEFAULTS = {
        "server": {
            "port":DEFAULT_SERVER_PORT,
        },

        "logging": {
            "print_logs":True,
            "write_logs":True,
            "print_logs_from_level":2,
            "write_logs_from_level":0
        },

        "game": {
            "name":"GiGaia Server",
            "description":"Join me!",
            "theme_color":[198, 140, 83],

            "tickrate": 60,
            "login_attempts": 5,
            "entity_visibility_range": 6
        },

        "world": {
            "name":f"World_{os.urandom(3).hex()}",
            "serve_range":8,
            "generator": SETTINGS,
            "chunk_tile_mod_max": 5,
        }  
    }

    def __init__(self, config_dir):

        self.path = config_dir

        self.create_config_structure()
        self.load()

    def get_config_filepath(self,conf_type: str):
        return os.path.join(self.path, conf_type+".json")

    def create_config_structure(self):

        for conf_type, conf in self.__DEFAULTS.items():

            conf_path = self.get_config_filepath(conf_type)

            if not os.path.exists(conf_path):

                with open(conf_path, "w") as cf:

                    json.dump(conf, cf, indent=4)

    def load(self):

        for conf_type, default_conf in self.__DEFAULTS.items():

            conf_path = self.get_config_filepath(conf_type)

            with open(conf_path, "r") as cf:
                conf = {**default_conf, **json.load(cf)}

            setattr(self, conf_type, SimpleNamespace(**conf))
