
from GiGaia.GiClient.UI.Widgets.text import Message

import pygame

class EntityName(Message):

    def __init__(self, ui_manager, entity, ui_frame):
        super().__init__(ui_manager, text=entity.props['name'], text_scale=2, font="basic", position=(0,0), anchor="center", relative_to=ui_frame)
        
        self.entity = entity

    def update(self):

        if not self.entity.exists:
            self.delete()

        if self.entity.props["name"] != self.text:
            self.change(self.entity.props["name"])

        self.position = (int(self.entity.window_pos[0]), int(self.entity.window_pos[1])-60)