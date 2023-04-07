from ..menupage import MenuPage

from GiGaia.GiClient.UI.Widgets.Menu.title import Title
from GiGaia.GiClient.UI.Widgets.Menu.button import PageLink, ActionButton
from GiGaia.GiClient.UI.Widgets.Menu.message import Message

from GiGaia.GiCore import INFO

class Info(MenuPage):

    def __init__(self, menu):
        super().__init__(menu, "Start")

    def enter(self):

        pass

    def create(self):

        self.uim.add_widget(Title, self.w, "Information")

        self.msg = self.uim.add_widget(Message, self.w, INFO, [0.5, 0.5], text_scale=2)

        self.uim.add_widget(ActionButton, self.w, "Ok!", action=self.back, position=[0.5, 0.85])