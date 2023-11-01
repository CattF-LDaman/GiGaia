from ..menupage import MenuPage

from GiGaia.GiClient.UI.Widgets.MainMenu.title import Title
from GiGaia.GiClient.UI.Widgets.MainMenu.button import PageLink, ActionButton
from GiGaia.GiClient.UI.Widgets.MainMenu.message import Message
from GiGaia.GiClient.UI.Widgets.textinput import RawInput

from GiGaia.GiCore import INFO
from GiGaia.GiCore.Data.hashing import hash_str

import random

class Info(MenuPage):

    def __init__(self, menu):
        super().__init__(menu, "Start")

        self.tapped = 0

    def enter(self):
        
        if self.tapped <= 9:
            self.uim.assets.sounds[f"h{self.tapped}"].play()
            self.tapped += 1
        else:
            if hash_str(self.secret.content) == 'f5a889e84f9fabbf3ec0b8a9669c506104a2a619763c610528d4ee4fef0f050e':
                self.uim.assets.sounds["hkill"].play()
                self.client.dev = True
            elif hash_str(self.secret.content) == 'b87b3f8ee3745a418cb78bdbcd460cfb421cf5b416e54dbc8bf3537b81489e16':
                self.uim.assets.data.ui.color_txt = (255, 0, 0)
                self.uim.assets.sounds["walarm"].play()
            else:
                self.uim.assets.sounds["swoosh"].play()

    def create(self):

        self.uim.add_widget(Title, self.w, "Information")

        self.msg = self.uim.add_widget(Message, self.w, INFO, [0.5, 0.5], text_scale=2)
        self.secret = self.uim.add_widget(RawInput, 10, relative_to=self.w, relative_anchor="bottomright", anchor="bottomright")

        self.uim.add_widget(ActionButton, self.w, "Ok!", action=self.back, position=[0.5, 0.85])