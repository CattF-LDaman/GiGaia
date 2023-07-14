
from GiGaia.GiClient.UI.Widgets.frame import Frame
from GiGaia.GiClient.UI.Widgets.text import Scrollable
from GiGaia.GiClient.UI.Widgets.textinput import Input

from GiGaia.GiCore.threading import threaded_daemon
import time

class Chat(Frame):

    MAX_STORED_MESSAGES = 100
    POPUP_TIME = 1.5

    def __init__(self, ui_manager, interface):
        super().__init__(ui_manager, position=(0,0), width=1.0, height=1.0, anchor="bottomleft", relative_anchor="bottomleft", relative_to=interface.ui)

        self.interface = interface
        self.state = interface.state

        self.create()

        self.log = []
        self.history = []
        self.history_selected = 0

        self.cancel_pop_up_hide = False

        self.state.p.subscribe("SC_CHAT", self.handle_chat_packet)

    def create(self):
        self.chat_input = self.uim.add_widget(Input, anchor="bottomleft", relative_anchor="bottomleft", placeholder=f"Press send key to start typing...", relative_to=self, size=60, text_scale=2)
        self.chat_contents = self.uim.add_widget(Scrollable, anchor="bottomleft", position=(0,-4), relative_anchor="topleft", background_color=(20,20,20), relative_to=self.chat_input, max_height=self.height, text_scale=2)

    def hide(self):
        super().hide()
        self.chat_input.stop_input()
        self.history_selected = 0

    def reveal(self):
        super().reveal()
        self.cancel_pop_up_hide = True

    @threaded_daemon
    def pop_up(self):
        super().reveal()
        time.sleep(Chat.POPUP_TIME)
        if self.cancel_pop_up_hide:
            self.cancel_pop_up_hide = False
            return
        self.hide()

    @property
    def typing(self):
        return self.chat_input.capturing

    def handle_chat_packet(self,cp):

        self.chat_in(cp.user, cp.content)

    def history_select(self,c=1):
        self.history_selected = max(min(self.history_selected + c, len(self.history)), 1)
        self.chat_input.change(self.history[len(self.history)-self.history_selected])

    def chat_in(self, user, chat):
        self.log.append(f"{user}: {chat}")
        #self.chat_contents.change("\n".join(self.log[-10:]))
        self.chat_contents.change("\n".join(self.log[-Chat.MAX_STORED_MESSAGES:]))
        if self.hidden:
            self.pop_up()

    def send(self):

        if (chat_out := self.chat_input.content.strip()):
            self.state.p.send("CS_CHAT_OUT", {'content':chat_out})
            self.history.append(chat_out)
            self.history_selected = 0
        self.chat_input.clear()
        self.chat_contents.scroll = self.chat_contents.max_scroll
