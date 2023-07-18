
from .windows import Window

from GiGaia.GiClient.UI.Widgets.text import Message

class Inventory(Window):

    TITLE = "Inventory"

    def __init__(self, ui_manager, wman, layer):
        super().__init__(ui_manager, wman, size=(0.95, 0.8), closable=True, movable=False, layer=layer)

        self.interface = wman.interface
        self.game = self.interface.game

        self.selected_container = None

    def create(self):

        self.container_title = self.uim.add_widget(Message, text="", relative_to=self, position=(0,0.1), shadow=True, text_scale=3, layer=self.layer+1, relative_anchor="midtop", anchor="midtop")
        self.msg = self.uim.add_widget(Message, text=str(self.game.client.session_id), relative_to=self, layer=self.layer+1, relative_anchor="center", anchor="center")

    def update_window(self):

        if not self.selected_container and not self.state.inv.contents:
            return
        elif not self.selected_container:
            self.selected_container = list(self.state.inv.contents)[0]
        
        self.container_title.change(self.selected_container)
        self.msg.change(f"{self.selected_container}: {', '.join(str((i.NAME, i.ID, i.RARITY, i.amount)) for i in self.state.inv.contents[self.selected_container])}")
