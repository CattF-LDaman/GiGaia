
from ..menupage import MenuPage

from GiGaia.GiClient.UI.Widgets.MainMenu.title import Title
from GiGaia.GiClient.UI.Widgets.MainMenu.button import PageLink, ActionButton
#from GiGaia.GiClient.UI.Widgets.MainMenu.message import Message
from GiGaia.GiClient.UI.Widgets.text import Message

from GiGaia.GiClient.UI.Widgets.textinput import Input

import string

class Play(MenuPage):

    def __init__(self, menu):
        super().__init__(menu, "Start")

    def create(self):

        self.uim.add_widget(Title, self.w, "Play game")
        #self.uim.add_widget(Input, allowed_chars="1234567890.", position=[0.5, 0.5], width=600, height=200, anchor="center", always_redraw=True)
        self.uim.add_widget(PageLink, self.w, menu=self.menu, page_to="ConnectTo", text="Online", pos=0.2)
        self.uim.add_widget(PageLink, self.w, menu=self.menu, page_to="PlayLocal", text="Local", pos=0.4)

class ConnectTo(MenuPage):

    def __init__(self, menu):
        super().__init__(menu, "Play")

        self.inputs_order = []

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

    def tab(self):

        for inpn, inp in enumerate(self.inputs_order):
            if inp.capturing:
                inp.unclicked = True
                self.inputs_order[inpn+1 if inpn != len(self.inputs_order)-1 else 0].clicked = True

    def create(self):

        self.uim.add_widget(Title, self.w, "Join server")

        self.msg = self.uim.add_widget(Message, relative_to=self.w, text="", position=[0.5, 0.15], text_scale=2)

        last_user = self.menu.last_username
        if self.menu.last_server:
            last_ip = self.menu.last_server[0]
            last_port = str(self.menu.last_server[1])
        else:
            last_ip = last_port = None

        self.user_in = self.uim.add_widget(Input, size=30, allowed_chars=string.ascii_letters+string.digits, default=last_user if last_user else "", text_scale=2, position=[0, 0.3], name="Username", anchor="center", relative_anchor="midtop", relative_to=self.w)

        self.ip_in = self.uim.add_widget(Input, size=30, allowed_chars=None, default=last_ip if last_ip else "", text_scale=2, position=[0, 0.4], name="IP", anchor="center", relative_anchor="midtop", relative_to=self.w)
        self.port_in = self.uim.add_widget(Input, size=5, isize_w=self.user_in.size[0], allowed_chars="0123456789", text_scale=2, position=[0, 0.5], name="Port", default=str(self.menu.config.networking.default_port) if not last_port else last_port, anchor="center", relative_anchor="midtop", relative_to=self.w)

        self.inputs_order = [self.user_in, self.ip_in, self.port_in]

        self.uim.add_widget(ActionButton, self.w, "Join", action=self.enter, position=[0.5, 0.85])

class PlayLocal(MenuPage):

    def __init__(self, menu):
        super().__init__(menu, "Play")

    def create(self):

        self.uim.add_widget(Title, self.w, "Play Local")

        self.msg = self.uim.add_widget(Message, relative_to=self.w, text="Under construction...", position=[0.5, 0.15], text_scale=2)


class Joining(MenuPage):

    def __init__(self, menu):
        super().__init__(menu, "ConnectTo")

        self.cancel_button = None

    def enter(self):

        pass

    def update(self):

        self.msg.change(self.menu.join_status)

        if self.menu.join_failed:

            self.msg.color = self.uim.assets.data.ui.color_err
            self.msg.change("Failed.")
            self.err_msg.change(self.menu.join_status)

            if not self.cancel_button:
                self.cancel_button = self.uim.add_widget(ActionButton, self.w, "Back", action=self.back, position=[0.5, 0.85])
        
        self.msg.adapt_size()


    def create(self):

        self.uim.add_widget(Title, self.w, "Join server")

        self.msg = self.uim.add_widget(Message, relative_to=self.w, text="", position=[0.5, 0.35], text_scale=4)
        self.err_msg = self.uim.add_widget(Message, relative_to=self.w, text="", position=[0.5, 0.5], color=self.uim.assets.data.ui.color_err, text_scale=3)

        #self.uim.add_widget(ActionButton, self.w, "Cancel", action=self.enter, position=[0.5, 0.85])