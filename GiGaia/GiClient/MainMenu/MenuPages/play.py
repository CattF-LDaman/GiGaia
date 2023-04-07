
from ..menupage import MenuPage

from GiGaia.GiClient.UI.Widgets.Menu.title import Title
from GiGaia.GiClient.UI.Widgets.Menu.button import PageLink, ActionButton
from GiGaia.GiClient.UI.Widgets.Menu.message import Message

from GiGaia.GiClient.UI.Widgets.textinput import Input

class Play(MenuPage):

    def __init__(self, menu):
        super().__init__(menu, "Start")

    def create(self):

        self.uim.add_widget(Title, self.w, "Play game")
        #self.uim.add_widget(Input, allowed_chars="1234567890.", position=[0.5, 0.5], width=600, height=200, anchor="center", always_redraw=True)
        self.uim.add_widget(PageLink, self.w, menu=self.menu, page_to="ConnectTo", text="Online", pos=0.2)
        self.uim.add_widget(PageLink, self.w, menu=self.menu, page_to="ConnectTo", text="Local", pos=0.4)

class ConnectTo(MenuPage):

    def __init__(self, menu):
        super().__init__(menu, "Play")

    def enter(self):

        user = self.user_in.content.strip()

        ip = self.ip_in.content.strip()

        port = int(self.port_in.content.strip())

        if port < 0 and port > 65535:
            self.msg.text = "Port should be a whole number from 0 to 65,535."
            self.msg.adapt_size()
            return

        addr = (ip, port)

        self.menu.start_join(addr, user)

    def create(self):

        self.uim.add_widget(Title, self.w, "Join server")

        self.msg = self.uim.add_widget(Message, self.w, "", [0.5, 0.15], text_scale=2)

        self.user_in = self.uim.add_widget(Input, size=30, allowed_chars=None, text_scale=2, position=[0, 0.3], name="Username", anchor="center", relative_anchor="midtop", relative_to=self.w)

        self.ip_in = self.uim.add_widget(Input, size=30, allowed_chars=None, text_scale=2, position=[0, 0.4], name="IP", anchor="center", relative_anchor="midtop", relative_to=self.w)
        self.port_in = self.uim.add_widget(Input, size=5, isize_w=self.user_in.size[0] , allowed_chars="0123456789", text_scale=2, position=[0, 0.5], name="Port", default=str(self.menu.config.networking.default_port), anchor="center", relative_anchor="midtop", relative_to=self.w)

        self.uim.add_widget(ActionButton, self.w, "Join", action=self.enter, position=[0.5, 0.85])

class Joining(MenuPage):

    def __init__(self, menu):
        super().__init__(menu, "ConnectTo")

        self.cancel_button = None

    def enter(self):

        pass

    def update(self):

        self.msg.text = self.menu.join_status

        if self.menu.join_failed:
            self.msg.anchor = "center"
            self.msg.relative_anchor = "center"
            self.msg.position = [0,0]
            self.msg.text_scale = 2

            if not self.cancel_button:
                self.cancel_button = self.uim.add_widget(ActionButton, self.w, "Back", action=self.back, position=[0.5, 0.85])
        
        self.msg.adapt_size()


    def create(self):

        self.uim.add_widget(Title, self.w, "Join server")

        self.msg = self.uim.add_widget(Message, self.w, "", [0.5, 0.35], text_scale=4)

        #self.uim.add_widget(ActionButton, self.w, "Cancel", action=self.enter, position=[0.5, 0.85])