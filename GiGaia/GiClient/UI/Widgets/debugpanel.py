
from GiGaia.GiClient.UI.widget import Widget
from GiGaia.GiClient import CLIENT_STATE_INGAME, CLIENT_STATE_MENU

from GiGaia.GiCore import VERSION_STRING
from GiGaia.GiCore.Game.states import STATE_IDS as SIDS
from GiGaia.GiCore.Game.World.coords import diff_coords, sum_coords, mult_coord, div_coord
from GiGaia.GiCore.Game.World import CHUNK_SIZE_PIXELS, TILE_SIZE_PIXELS

import time
import pygame

class DebugPanel(Widget):

    def __init__(self, ui_manager):

        super().__init__(ui_manager, position=[0, 16], layer=32, width=1.0, height=0.6, anchor="topleft", always_redraw=True)

        self.contents = {}

        self.fps_s = 0
        self.last_fps_time = 0

        self.hud = None

    def update(self):

        if time.time() - self.last_fps_time > 1:
            self.fps_s = int(self.client.clock.get_fps())
            self.last_fps_time = time.time()

        self.contents = {
            "version": VERSION_STRING,
            "WARNING": 'This debug panel lowers your performance! Use F3 for FPS counter.',
            "pygame-ce":pygame.version.ver,
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
                    "cursor_wpos": gamestate.scene.mouse,
                    "cursor_tpos": div_coord(gamestate.scene.mouse, TILE_SIZE_PIXELS, floor=True),
                    "player_wpos": gamestate.player.position,
                    "player_tpos": gamestate.player.tile_pos,
                    "player_cpos": gamestate.player.chunk_pos,
                    "delta_pos": diff_coords(gamestate.scene.camera_pos, gamestate.player.position),
                    "tile_upd": f"{gamestate.world.tile_updates}/{self.client.config.world.max_tile_updates_per_tick}",
                    "chunks_drawn": gamestate.world.viewport_size,
                    "time": gamestate.world.time.value,
                    "day": gamestate.world.time.day,
                    "day_progress": gamestate.world.time.day_progress,
                    "night": gamestate.world.time.is_night
                }

                if not self.hud:
                    self.hud = self.uim.add_widget(DebugHUD, self, gamestate)
        
        elif self.client.state == CLIENT_STATE_MENU:
            self.contents |= {"page": self.client.menu.page.__class__.__name__}


    def draw(self):

        self.surface.fill(self.uim.assets.data.ui.colorkey)
        for cn, (ck, cv) in enumerate(self.contents.items()):
            self.uim.assets.fonts["basic"].render(self.surface, (4, int(self.size[1]/len(self.contents)*cn)), f"{ck}:{cv}", scale=1)

class DebugHUD(Widget):

    def __init__(self, ui_manager, panel, gamestate):

        super().__init__(ui_manager, position=[0, 0], layer=31, width=1.0, height=1.0, anchor="topleft", always_redraw=True, child_of=panel)

        self.gamestate = gamestate
        self.game_scale = 0

    def update(self):

        pass

    def show_chunk(self, cp):
        chunk = self.gamestate.world.chunks[cp]
        cr = pygame.Rect(chunk.draw_pos[0]*self.game_scale, chunk.draw_pos[1]*self.game_scale, CHUNK_SIZE_PIXELS*self.game_scale, CHUNK_SIZE_PIXELS*self.game_scale)
        self.uim.assets.fonts["basic"].render(self.surface, mult_coord(chunk.draw_pos, self.game_scale), str(chunk.position), scale=1)
        self.uim.assets.fonts["basic"].render(self.surface, mult_coord(sum_coords(chunk.draw_pos,(0,10)), self.game_scale) , str(chunk.world_position), scale=1)
        pygame.draw.rect(self.surface, (160,160,255), cr, width=1)
        if chunk.tile_updates:
            pygame.draw.rect(self.surface, (255,160,160), cr, width=4, border_radius=6)

    def show_ent(self, ent):
        self.uim.assets.fonts["basic"].render(self.surface, sum_coords(ent.window_pos, (0,-10)), str(ent.instance_id), scale=1, blit_anchor_center=True)
        self.uim.assets.fonts["basic"].render(self.surface, sum_coords(ent.window_pos, (0,10)), str(ent.NAME), scale=1, blit_anchor_center=True)
        self.uim.assets.fonts["basic"].render(self.surface, sum_coords(ent.window_pos, (0,20)), str(ent.position), scale=1, blit_anchor_center=True)
        if "width" in ent.props:
            er = pygame.Rect(0,0,ent.props['width']*self.game_scale, ent.props['height']*self.game_scale)
            er.center = ent.window_pos
            pygame.draw.rect(self.surface, (100,255,100), er, width=1)
            if er.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.surface, (255,120,255), er, width=5)
                self.uim.assets.fonts["basic"].render(self.surface, pygame.mouse.get_pos(), '\n'.join(f'{k}: {v}' for k,v in ent.props.items()), scale=1, blit_anchor_center=True)

    def draw(self):

        self.surface.fill(self.uim.assets.data.ui.colorkey)
        
        self.game_scale = self.client.config.client.game_scale

        for cp in self.gamestate.world.get_viewport_chunks():
            if cp in self.gamestate.world.chunks:
                self.show_chunk(cp)
        
        for ent in self.gamestate.entity_manager.entities.values():
            self.show_ent(ent)