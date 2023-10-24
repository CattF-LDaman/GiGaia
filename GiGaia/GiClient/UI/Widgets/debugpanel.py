
from GiGaia.GiClient.UI.widget import Widget
from GiGaia.GiClient import CLIENT_STATE_INGAME, CLIENT_STATE_MENU

from GiGaia.GiCore import VERSION_STRING
from GiGaia.GiCore.Game.states import STATE_IDS as SIDS
from GiGaia.GiCore.Game.World.coords import diff_coords

import time
import pygame

class DebugPanel(Widget):

    def __init__(self, ui_manager):

        super().__init__(ui_manager, position=[0, 16], layer=32, width=1.0, height=0.6, anchor="topleft", always_redraw=True)

        self.contents = {}

        self.fps_s = 0
        self.last_fps_time = 0

    def update(self):

        if time.time() - self.last_fps_time > 1:
            self.fps_s = int(self.client.clock.get_fps())
            self.last_fps_time = time.time()

        self.contents = {
            "version": VERSION_STRING,
            "state": self.client.state,
            "fps": int(self.client.clock.get_fps()),
            "fps_s": self.fps_s,
            "res":self.client.window.get_size(),
            "dt": self.client.dt,
            "dt_ms": self.client.dt_ms,
            "dt_var": self.client.dt_var,
            "ms": self.client.ticks,
            "s": self.client.ticks//1000,
            "widgets": ', '.join([str(widget.__class__.__name__) for layer in self.uim.widgets for widget in layer]),
            "uidraws": self.uim.redraws
        }

        if self.client.state == CLIENT_STATE_INGAME:
            gamestate = self.client.game.state

            self.contents |= {
                "server": self.client.game.addr[0],
                "sent":self.client.game.postman.sent,
                "recv":self.client.game.postman.received,
                "drop":self.client.game.postman.dropped,
                "frag":self.client.game.postman.conn.fragmentations,
                "ping":self.client.game.postman.ping,
                "mpexpire": min(int(self.client.dt_ms+self.client.dt_var+(self.client.game.postman.ping/2)+5), 600),
                "user": self.client.game.username,
                "gamestate": type(gamestate).__name__
            }

            if gamestate.sid == SIDS.PLAYING:

                self.contents |= {
                    "entities": len(gamestate.entity_manager.entities),
                    "player": gamestate.player_eid,
                    "cam": gamestate.scene.camera_pos,
                    "cursor_wpos": gamestate.scene.convert_window_to_world_coord(pygame.mouse.get_pos()),
                    "player_wpos": gamestate.player.position,
                    "player_tpos": gamestate.player.tile_pos,
                    "player_cpos": gamestate.player.chunk_pos,
                    "delta_pos": diff_coords(gamestate.scene.camera_pos, gamestate.player.position),
                    "chunks_upd": f"{gamestate.world.surface_updates}/{self.client.config.world.max_chunk_updates_per_tick}",
                    "chunks_drawn": gamestate.world.viewport_size,
                    "time": gamestate.world.time.value,
                    "day": gamestate.world.time.day,
                    "day_progress": gamestate.world.time.day_progress,
                    "night": gamestate.world.time.is_night
                }
        
        elif self.client.state == CLIENT_STATE_MENU:
            self.contents |= {"page": self.client.menu.page.__class__.__name__}


    def draw(self):

        self.surface.fill(self.uim.assets.data.ui.colorkey)
        for cn, (ck, cv) in enumerate(self.contents.items()):
            self.uim.assets.fonts["basic"].render(self.surface, (4, int(self.size[1]/len(self.contents)*cn)), f"{ck}:{cv}", scale=1)
