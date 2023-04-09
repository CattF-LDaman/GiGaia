
from GiGaia.GiClient.UI.widget import Widget

from GiGaia.GiClient.UI.Widgets.Menu.message import Message

class GameTitle(Message):

    def __init__(self, ui_manager, pagew):

        super().__init__(ui_manager, pagew, text="GiGaia", position=(0.5,0), text_scale=4, color=ui_manager.assets.data.ui.color_txt, font="fat")

class Title(Message):

    def __init__(self, ui_manager, pagew, text):

        self.text = text
        super().__init__(ui_manager, pagew, text=text, position=(0.5,0.05), text_scale=4, color=None)