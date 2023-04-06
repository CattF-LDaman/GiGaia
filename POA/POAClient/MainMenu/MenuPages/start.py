
from ..menupage import MenuPage

from POA.POAClient.UI.Widgets.Menu.title import GameTitle
from POA.POAClient.UI.Widgets.Menu.button import PageLink, ActionButton

class Start(MenuPage):

    def __init__(self, menu):
        super().__init__(menu)


    def quit(self):
        self.menu.client.close()

    def create(self):

        self.uim.add_widget(GameTitle, self.w)
        #self.uim.add_widget(Input, allowed_chars="1234567890.", position=[0.5, 0.5], width=600, height=200, anchor="center", always_redraw=True)
        self.uim.add_widget(PageLink, self.w, menu=self.menu, page_to="Play", text="Play", pos=0.2)
        self.uim.add_widget(PageLink, self.w, menu=self.menu, page_to="Info", text="Info", pos=0.4)
        self.uim.add_widget(ActionButton, self.w, "Exit", action=self.quit, position=[0.5, 0.6], text_color=(180,180,180))

