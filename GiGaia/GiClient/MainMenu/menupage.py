
from GiGaia.GiClient.UI.Widgets.MainMenu.page import PageWidget
from GiGaia.GiClient.UI.Widgets.MainMenu.button import BackButton

class MenuPage:
    """
        Base class for MenuPages, these create widgets and handle logic for MainMenu UI.
    """

    def __init__(self, menu, prev_page=None):

        self.menu = menu
        self.client = menu.client
        self.ui_manager = self.uim = menu.uim

        self.w = self.uim.add_widget(PageWidget)

        self.prev_page = prev_page
        if prev_page:
            self.uim.add_widget(BackButton, self.w, self.back)

    def back(self):
        if self.prev_page:
            self.menu.switch(self.prev_page)

    def enter(self):

        pass

    def create(self):

        pass

    def update(self):

        pass

    def destroy(self):

        self.w.delete()