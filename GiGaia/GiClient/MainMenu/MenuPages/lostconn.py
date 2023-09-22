from ..menupage import MenuPage

from GiGaia.GiClient.UI.Widgets.MainMenu.title import Title
from GiGaia.GiClient.UI.Widgets.MainMenu.message import Message

from GiGaia.GiClient.UI.Widgets.button import ActionButton
from GiGaia.GiClient.UI.Widgets.frame import ColorFrame

class LostConn(MenuPage):

    def __init__(self, menu):
        super().__init__(menu, "Start")

    def reconnect(self):

        self.menu.start_join(self.menu.last_server, self.menu.last_username)

    def create(self):

        self.uim.add_widget(Title, self.w, "Oops!")

        self.msg = self.uim.add_widget(Message, self.w, self.menu.lost_connection, [0.5, 0.5], text_scale=2)
        self.menu.lost_connection = None

        butt_frame = self.uim.add_widget(ColorFrame, position=[0, 0.8], anchor="center", relative_anchor="midtop", width=0.9, height=80, fill_color=self.uim.assets.data.ui.color_B0, relative_to=self.w)

        self.uim.add_widget(ActionButton, text="Ok", width=0.40, height=60, action=self.back, position=[10, 0], anchor="midleft", relative_anchor="midleft", relative_to=butt_frame, layer=31)
        self.uim.add_widget(ActionButton, text="Retry", width=0.40, height=60, action=self.reconnect, position=[-10, 0], anchor="midright", relative_anchor="midright", relative_to=butt_frame, layer=31)
        # self.uim.add_widget(ActionButton, self.w, "Ok", action=self.back, position=[0.5, 0.85])
        # self.uim.add_widget(ActionButton, self.w, "Reconnect", action=self.back, position=[0.5, 0.85])