
from GiGaia.GiClient.Game.interface import Interface

from GiGaia.GiClient.UI.Widgets.panel import Panel
from GiGaia.GiClient.UI.Widgets.textinput import Input
from GiGaia.GiClient.UI.Widgets.button import ActionButton
from GiGaia.GiClient.UI.Widgets.text import Message
from GiGaia.GiClient.UI.Widgets.frame import Frame

class Playing(Interface):

    def __init__(self, state):
        super().__init__(state)

    def create(self):

        self.p = self.uim.add_widget(Panel)

        self.uim.add_widget(Message, text="GiGaia", text_scale=5, position=[0, 0], anchor="center", relative_anchor="center", relative_to=self.p)
