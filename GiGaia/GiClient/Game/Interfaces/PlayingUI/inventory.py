
from .windows import Window

from GiGaia.GiClient.UI.Widgets.text import Message

class Inventory(Window):

    TITLE = "Inventory"

    def __init__(self, ui_manager, wman, layer):
        super().__init__(ui_manager, wman, size=(0.95, 0.8), closable=True, movable=True, layer=layer)

        self.interface = wman.interface
        self.game = self.interface.game

    def create(self):

        self.msg = self.uim.add_widget(Message, text=str(self.game.client.session_id), relative_to=self, layer=self.layer+1, relative_anchor="center", anchor="center")

    def update_window(self):

        self.msg.change(str(self.state.inv))
