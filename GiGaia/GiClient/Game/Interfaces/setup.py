
from GiGaia.GiClient.Game.interface import Interface

from GiGaia.GiClient.UI.Widgets.frame import Frame
from GiGaia.GiClient.UI.Widgets.panel import Panel
from GiGaia.GiClient.UI.Widgets.textinput import Input
from GiGaia.GiClient.UI.Widgets.button import ActionButton
from GiGaia.GiClient.UI.Widgets.text import Message

class Setup(Interface):

    def __init__(self, state):
        super().__init__(state)

    def submit(self):

        if not self.state.game_info.user_exist:
            if self.pwd_in.content != self.pwd_conf_in.content:
                self.error_msg.change("Passwords don't match!")
                return

        OK = self.state.submit(self.pwd_in.content)

        if not OK.is_ok:
            self.error_msg.change(OK.msg)

    def destroy(self):
        
        self.p.delete()

    def create(self):
        ginf = self.state.game_info

        self.game.background = ginf.theme_color

        self.p = self.uim.add_widget(Panel)

        self.uim.add_widget(Message, text=f"{'''Let's get started.''' if not ginf.user_exist else f'Welcome back, {self.state.game.username}'}\nEnter your password.", text_scale=2, position=[0, 0.05], anchor="midtop", relative_anchor="midtop", relative_to=self.p)
        self.error_msg = self.uim.add_widget(Message, text="", text_scale=2, color=(255,0,0), position=[0, 0.1], anchor="midtop", relative_anchor="midtop", relative_to=self.p)
        
        self.info_frame = self.uim.add_widget(Frame, position=[0, 0.15], width=0.8, height=120, anchor="midtop", relative_anchor="midtop", relative_to=self.p, skip_event=True)
        
        self.server_name = self.uim.add_widget(Message, text=ginf.name, color=ginf.theme_color, text_scale=4, position=[0, 0], anchor="center", relative_anchor="midtop", relative_to=self.info_frame)
        self.server_description = self.uim.add_widget(Message, text=ginf.description, text_scale=2, position=[0, 0], anchor="center", relative_anchor="center", relative_to=self.info_frame)
        self.server_connected = self.uim.add_widget(Message, text=f"{ginf.connected-1} online", text_scale=2, position=[0, 0], anchor="center", relative_anchor="midbottom", relative_to=self.info_frame)
        
        self.pwd_frame = self.uim.add_widget(Frame, position=[0, 0.1], width=0.8, height=200, anchor="center", relative_anchor="center", relative_to=self.p, skip_event=True)
        self.pwd_in = self.uim.add_widget(Input, size=32, show="*", text_scale=2, position=[0, 0.1], name="Password", anchor="center", relative_anchor="midtop", relative_to=self.pwd_frame)
        if not ginf.user_exist:
            self.pwd_conf_in = self.uim.add_widget(Input, size=32, show="*", text_scale=2, position=[0, 0.8], name="Password again", anchor="center", relative_anchor="midtop", relative_to=self.pwd_frame)
        
        #self.hello_in = self.uim.add_widget(Input, size=32, placeholder=f"eg. Goodmorning everyone!", text_scale=2, position=[0, 0.4], name="Hello message", anchor="center", relative_anchor="midtop", relative_to=self.p)

        self.uim.add_widget(ActionButton, text="Go!", action=self.submit, position=[0, 0.9], anchor="center", relative_anchor="midtop", relative_to=self.p)


