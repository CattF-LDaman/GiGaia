
from POA.POAClient.UI.widget import Widget

class DevIndicator(Widget):

    def __init__(self, ui_manager):

        super().__init__(ui_manager, position=[0.96, 0.96], layer=31, width=60, height=40, anchor="center", always_redraw=False)


    def update(self):

        pass

    def draw(self):

        self.surface.fill(self.uim.assets.data.ui.colorkey)
        self.uim.assets.fonts["basic"].render(self.surface, (0,0) , f"DEV", scale=2, color=(190,190,190))
