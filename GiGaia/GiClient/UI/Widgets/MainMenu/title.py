
from GiGaia.GiClient.UI.Widgets.MainMenu.message import Message

import math

class GameTitle(Message):

    def __init__(self, ui_manager, pagew):

        super().__init__(ui_manager, pagew, text="GiGaia", position=(0.5,0), text_scale=4, shadow=True, shadow_color=(31, 96, 64), color=ui_manager.assets.data.ui.color_txt, font="fat")

    def update(self):
        
        self.position[1] = -abs(math.sin(self.age/400))/30

class Title(Message):

    def __init__(self, ui_manager, pagew, text):

        self.text = text
        super().__init__(ui_manager, pagew, text=text, position=(0.5,-0.05), text_scale=2, color=None, shadow=True, shadow_color=(100,100,100), font="fat")