
from GiGaia.GiClient.Game.interface import Interface

from GiGaia.GiClient.UI.Widgets.panel import Panel
from GiGaia.GiClient.UI.Widgets.textinput import Input
from GiGaia.GiClient.UI.Widgets.button import ActionButton
from GiGaia.GiClient.UI.Widgets.text import Message

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

        self.uim.add_widget(Message, text="Let's get started.\nEnter your password.", text_scale=2, position=[0, 0.05], anchor="midtop", relative_anchor="midtop", relative_to=self.p)
        self.error_msg = self.uim.add_widget(Message, text="", text_scale=2, position=[0, 0.1], anchor="midtop", relative_anchor="midtop", relative_to=self.p)

        self.pwd_in = self.uim.add_widget(Input, size=32, placeholder=f"eg. {self.game.username.capitalize()} Empire", text_scale=2, position=[0, 0.3], name="Password", anchor="center", relative_anchor="midtop", relative_to=self.p)
        #self.hello_in = self.uim.add_widget(Input, size=32, placeholder=f"eg. Goodmorning everyone!", text_scale=2, position=[0, 0.4], name="Hello message", anchor="center", relative_anchor="midtop", relative_to=self.p)

        self.uim.add_widget(ActionButton, text="Go!", action=self.submit, position=[0, 0.85], anchor="center", relative_anchor="midtop", relative_to=self.p)
