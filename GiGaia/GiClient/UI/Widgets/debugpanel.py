
from GiGaia.GiClient.UI.widget import Widget
from GiGaia.GiClient import CLIENT_STATE_INGAME, CLIENT_STATE_MENU

from GiGaia.GiCore import VERSION_STRING

import time

class DebugPanel(Widget):

    def __init__(self, ui_manager):

        super().__init__(ui_manager, position=[0, 16], layer=31, width=ui_manager.ui_layer.get_width(), height=150, anchor="topleft", always_redraw=True)

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
            "ms": self.client.ticks,
            "s": self.client.ticks//1000,
            "widgets": ', '.join([str(widget.__class__.__name__) for layer in self.uim.widgets for widget in layer]),
            "uidraws": self.uim.redraws
        }

        if self.client.state == CLIENT_STATE_INGAME:
            self.contents |= {
                "server": self.client.game.addr[0],
                "sent":self.client.game.postman.sent,
                "recv":self.client.game.postman.received,
                "drop":self.client.game.postman.dropped,
                "user": self.client.game.username,
                "gamestate": self.client.game.state
            }
        
        elif self.client.state == CLIENT_STATE_MENU:
            self.contents |= {"page": self.client.menu.page.__class__.__name__}


    def draw(self):

        self.surface.fill(self.uim.assets.data.ui.colorkey)
        for cn, (ck, cv) in enumerate(self.contents.items()):
            self.uim.assets.fonts["basic"].render(self.surface, (4, int(self.size[1]/len(self.contents)*cn)), f"{ck}:{cv}", scale=1)
