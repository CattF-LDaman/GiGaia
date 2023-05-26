from GiGaia.GiClient.UI.widget import Widget

class Frame(Widget):  # A logical widget to help structure UI

    def __init__(self, ui_manager, position=(0,0), width=0, height=0, anchor='topleft', relative_anchor='topleft', **kwargs):

        super().__init__(ui_manager, position=position, width=width, height=height, relative_anchor=relative_anchor, anchor=anchor, skip_draw=True, **kwargs)

class ColorFrame(Widget):  # A frame but filled with 'fill_color'

    def __init__(self, ui_manager, position=(0,0), width=0, height=0, anchor='topleft', relative_anchor='topleft', fill_color=(255,0,0), **kwargs):

        super().__init__(ui_manager, position=position, width=width, height=height, relative_anchor=relative_anchor, anchor=anchor, **kwargs)

        self.fill_color = fill_color

    def draw(self):

        self.surface.fill(self.fill_color)