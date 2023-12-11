
from GiGaia.GiCore.logging import Logger

DEFAULT_CONFIG = {

    "client": {
        "max_fps": 0,
        "window_width": 1000,
        "window_height": 800,
        "window_fullscreen": False,
        "game_scale": 2,
    },

    "logging": Logger.DEFAULT_CONFIG,

    "networking": {
        "default_port": 17746,
        "entity_ghosting": True,
        "entity_ghost_speed": 25,
        "player_ghost_speed": 50
    },

    "world": {
        "max_tile_updates_per_tick": 144,
        "viewport_padding": 20,
    }
}