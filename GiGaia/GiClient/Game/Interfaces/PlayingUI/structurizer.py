
from .windows import Window

from GiGaia.GiClient.UI.Widgets.button import ActionButton
from GiGaia.GiClient.UI.Widgets.frame import Frame, ColorFrame
from GiGaia.GiClient.UI.Widgets.textinput import Input
from GiGaia.GiClient.UI.Widgets.text import Message
from GiGaia.GiClient.UI.widget import Widget

from GiGaia.GiCore.Game.World.coords import rect_size, area, inside, sub_coords
from GiGaia.GiCore.Game.World.structuredata import StructureData

import os

class Structurizer(Window):

    TITLE = "Structurizer"

    def __init__(self, ui_manager, wman, layer):
        super().__init__(ui_manager, wman, size=(600, 800), closable=True, movable=False, layer=layer)
        
        self.world = self.state.world

    def save_structure(self):
        
        if not all(self.interface.structurizer_points):
            self.save_msg.change("Structure needs start and end.")
            return
        
        if not self.interface.structurizer_core:
            self.save_msg.change("Structure needs core.")
            return

        start, end = self.interface.structurizer_points
        struc_core = self.interface.structurizer_core

        if not inside(struc_core, start, end):
            self.save_msg.change("Core must be inside area.")
            return
        core = sub_coords(struc_core, start)

        name, description, author = self.name_in.content, self.desc_in.content, self.auth_in.content

        sdata = StructureData(os.path.join(self.game.client.dirs["structures"], name+'.gigs'))
        sdata.create(self.world, start, end, core, author, description)
        self.save_msg.change("Structure saved.")

    def reset_core(self):

        self.interface.structurizer_core = self.interface.structurizer_points[0]

    def create(self):

        self.strucinf = self.uim.add_widget(Message, text="", position=(0, 15), text_scale=2, relative_to=self, layer=self.layer+1, relative_anchor="midtop", anchor="midtop")
        inputs_frame = self.uim.add_widget(Frame, position=(0, 15), width=0.9, height=self.height-40-30, anchor='midtop', relative_anchor='midtop', relative_to=self, layer=self.layer+1)
        self.name_in = self.uim.add_widget(Input, size=32, text_scale=2, position=[0, 0.4], name="Name", anchor="center", relative_anchor="midtop", relative_to=inputs_frame, layer=self.layer+2)
        self.desc_in = self.uim.add_widget(Input, size=32, text_scale=2, position=[0, 0.5], name="Description", anchor="center", relative_anchor="midtop", relative_to=inputs_frame, layer=self.layer+2)
        self.auth_in = self.uim.add_widget(Input, size=32, text_scale=2, position=[0, 0.6], name="Author", anchor="center", relative_anchor="midtop", relative_to=inputs_frame, layer=self.layer+2)
        
        buttons_frame = self.uim.add_widget(ColorFrame, position=(0, -15), fill_color=self.uim.assets.data.ui.color_B0, width=0.9, height=80, anchor='midbottom', relative_anchor='midbottom', relative_to=self, layer=self.layer+1)
        self.save_msg = self.uim.add_widget(Message, text="", position=(0, -5), text_scale=2, relative_to=buttons_frame, layer=self.layer+1, relative_anchor="midtop", anchor="midbottom")
        save_btn = self.uim.add_widget(ActionButton, text="Save", text_color=self.uim.assets.data.ui.color_txt, action=self.save_structure, position=[0.05, 0], width=0.4, height=60, anchor="midleft", relative_anchor="midleft", relative_to=buttons_frame, layer=self.layer+2)
        core_btn = self.uim.add_widget(ActionButton, text="Core", text_color=self.uim.assets.data.ui.color_txt, action=self.reset_core, position=[-0.05, 0], width=0.4, height=60, anchor="midright", relative_anchor="midright", relative_to=buttons_frame, layer=self.layer+2)

    def update_window(self):
        
        strucsize = (0,0)
        strucarea = 0
        if all(self.interface.structurizer_points):
            strucsize = rect_size(*self.interface.structurizer_points)
            strucarea = area(*self.interface.structurizer_points)
        self.strucinf.change(f"Start: {self.interface.structurizer_points[0]}\nEnd: {self.interface.structurizer_points[1]}\nCore: {self.interface.structurizer_core}\nSize: {strucsize[0]}x{strucsize[1]}\nArea: {strucarea}")

# class StructurizerFrame(Widget):

#     def __init__(self, ui_manager, **kwargs):
#         super().__init__(ui_manager, position, layer, width, height, max_width, max_height, min_width, min_height, anchor, skip_event=True, **kwargs)