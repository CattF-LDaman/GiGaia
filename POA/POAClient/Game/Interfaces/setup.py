
from POA.POAClient.Game.interface import Interface

from POA.POAClient.UI.Widgets.panel import Panel
from POA.POAClient.UI.Widgets.textinput import Input
from POA.POAClient.UI.Widgets.button import ActionButton
from POA.POAClient.UI.Widgets.text import Message

class Setup(Interface):

    def __init__(self, state):
        super().__init__(state)

    def submit(self):

        OK = self.state.submit(self.nation_in.content, self.motto_in.content)

        if not OK.is_ok:
            self.error_msg.text = OK.msg
            self.error_msg.adapt_size()

    def create(self):

        self.p = self.uim.add_widget(Panel)

        self.uim.add_widget(Message, text="Let's get started.\nDefine your nation.", text_scale=2, position=[0, 0.05], anchor="midtop", relative_anchor="midtop", relative_to=self.p)
        self.error_msg = self.uim.add_widget(Message, text="", text_scale=2, position=[0, 0.1], anchor="midtop", relative_anchor="midtop", relative_to=self.p)

        self.nation_in = self.uim.add_widget(Input, size=32, placeholder=f"eg. {self.game.username.capitalize()} Empire", allowed_charset=True, text_scale=2, position=[0, 0.3], name="Name your nation", anchor="center", relative_anchor="midtop", relative_to=self.p)
        self.motto_in = self.uim.add_widget(Input, size=32, placeholder=f"eg. Victory is inevitable!", allowed_charset=True, text_scale=2, position=[0, 0.4], name="Nation motto", anchor="center", relative_anchor="midtop", relative_to=self.p)

        self.uim.add_widget(ActionButton, text="Go!", action=self.submit, position=[0, 0.85], anchor="center", relative_anchor="midtop", relative_to=self.p)
