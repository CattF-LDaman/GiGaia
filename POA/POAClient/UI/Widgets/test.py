
from POA.POAClient.UI.widget import Widget

class Test(Widget):

    def __init__(self, ui_manager, testp):

        super().__init__(ui_manager, position=[0.5, 0.5], width=600, height=200, anchor="center", always_redraw=False, vanish_after=2000)
        
        self.testp = testp

    def update(self):
        
        pass

    def draw(self):

        self.surface.fill(self.uim.assets.data.ui.colorkey)
        self.uim.assets.fonts["basic"].render(self.surface, (2,2) , self.testp.message, scale=2)
