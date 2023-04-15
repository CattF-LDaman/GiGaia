
from GiGaia.GiClient.UI.Widgets.text import Message

import pygame

class EntityName(Message):

    def __init__(self, ui_manager, entity, ui_frame):
        super().__init__(ui_manager, text=entity.props['name'], text_scale=2, font="basic", position=(0,0), anchor="center", relative_to=ui_frame)
        
        self.entity = entity

    def update(self):

        if not self.entity.exists:
            self.delete()

        self.position = (int(self.entity.draw_pos[0]), int(self.entity.draw_pos[1])-60)