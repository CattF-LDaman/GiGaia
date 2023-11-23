
from .windows import Window

from GiGaia.GiClient.UI.Widgets.text import Message
from GiGaia.GiClient.UI.Widgets.frame import Frame, ColorFrame
from GiGaia.GiClient.UI.widget import Widget

import itertools
import pygame

class Inventory(Window):

    TITLE = "Inventory"

    def __init__(self, ui_manager, wman, layer):
        super().__init__(ui_manager, wman, size=(0.95, 0.8), closable=True, movable=False, layer=layer)

        self.inventory = self.state.inv

        self.interface = wman.interface
        self.game = self.interface.game
        
        # self.selected_container = None

    def create(self):

        # self.container_title = self.uim.add_widget(Message, text="", relative_to=self, position=(0,0.1), shadow=True, text_scale=3, layer=self.layer+1, relative_anchor="midtop", anchor="midtop")
        # self.msg = self.uim.add_widget(Message, text=str(self.game.client.session_id), relative_to=self, layer=self.layer+1, relative_anchor="center", anchor="center")
        
        self.inv_panel = self.uim.add_widget(InventoryPanel, inv_ui=self)
        self.future_panel = self.uim.add_widget(ColorFrame, position=(-0.02, 0.05), fill_color=self.uim.assets.data.ui.color_B0, width=0.45, height=0.9, anchor='topright', relative_anchor='topright', relative_to=self, layer=self.layer+1)

    def update_window(self):

        pass
        # if not self.selected_container and not self.state.inv.contents:
        #     return
        # elif not self.selected_container:
        #     self.selected_container = list(self.state.inv.contents)[0]
        
        # self.container_title.change(self.selected_container)

        # nl = "\n"
        # self.msg.change(f"{self.selected_container}: {nl.join(str((i.NAME, i.ID, i.RARITY, i.amount)) for i in self.state.inv.contents[self.selected_container])}")

class InventoryPanel(ColorFrame):
    GRID_SPACING = 6
    HEADING_HEIGHT = 100

    def __init__(self, ui_manager, inv_ui):
        super().__init__(ui_manager, position=(0.02, 0.05), fill_color=inv_ui.uim.assets.data.ui.color_B, width=0.45, height=0.9, anchor='topleft', relative_anchor='topleft', relative_to=inv_ui, layer=inv_ui.layer+1)
        
        self.inv_ui = inv_ui
        self.inventory = inv_ui.state.inv

        self.selected_container = None
        self.container_title = self.uim.add_widget(Message, text="", relative_to=self, position=(0,0.1), shadow=True, text_scale=2, layer=self.layer+1, relative_anchor="midtop", anchor="midtop")

        self.grid_frame = self.uim.add_widget(Frame, width=0, height=0, relative_anchor='midbottom', anchor='midbottom', relative_to=self)
        self.grid = []

        self.create_grid()

    def create_grid(self):

        for invi in itertools.chain(*self.grid):
            invi.delete()
        self.grid_frame.children.clear()

        self.grid_frame.resize(w=(self.width//(InventoryItem.WIDTH+self.GRID_SPACING))*(InventoryItem.WIDTH+self.GRID_SPACING), h=self.height-self.HEADING_HEIGHT)
        self.grid = []

        grid_width = self.grid_frame.width//(InventoryItem.WIDTH+self.GRID_SPACING)
        grid_height = self.grid_frame.height//(InventoryItem.HEIGHT+self.GRID_SPACING)

        for row in range(grid_height):
            row_items = []
            for col in range(grid_width):
                item_x = col*(InventoryItem.WIDTH+self.GRID_SPACING)
                item_y = row*(InventoryItem.HEIGHT+self.GRID_SPACING)
                row_items.append(self.uim.add_widget(InventoryItem, None, position=(item_x, item_y), layer=self.layer+1, relative_to=self.grid_frame, anchor='topleft', relative_anchor='topleft'))
            self.grid.append(row_items)

    def handle_resize(self):
        self.create_grid()

    def update(self):

        if self.scrolled_down:
            print("DOWN")

        if self.scrolled_up:
            print("UP")

        if self.inventory.contents:
            if not self.selected_container:
                self.selected_container = list(self.inventory.contents)[0]
            for n, invi in enumerate(itertools.chain(*self.grid)):
                if n >= len(self.inventory.contents[self.selected_container]):
                    break
                item = self.inventory.contents[self.selected_container][n]
                if invi.item != item:
                    invi.change(self.inventory.contents[self.selected_container][n])

class InventoryItem(Widget):
    WIDTH = 120
    HEIGHT = 90

    ITEM_SPRITE_SCALE = 4

    def __init__(self, ui_manager, item, **kwargs):
        super().__init__(ui_manager, width=InventoryItem.WIDTH, height=InventoryItem.HEIGHT, **kwargs)

        self.item = item

        self.prev_amount = 0

    def change(self, item):
        self.item = item
        self.updated = True

    def update(self):

        if self.item:
            if self.item.amount != self.prev_amount:
                self.updated = True
                self.prev_amount = self.item.amount
    
    def draw(self):

        self.surface.fill(self.uim.assets.data.ui.color_B0)

        pygame.draw.rect(self.surface, self.item.RARITY_COLOR if self.item else self.uim.assets.data.ui.color_C, self.rect, width=5)

        if self.item:
            self.uim.assets.fonts["basic"].render(self.surface, (self.rect.midtop[0], 16) , str(self.item.amount), scale=2, color=self.item.RARITY_COLOR, blit_anchor_center=True)
            ISPRITE = pygame.transform.scale_by(self.item.SPRITE, InventoryItem.ITEM_SPRITE_SCALE)
            ISPRITE_RECT = ISPRITE.get_rect()
            ISPRITE_RECT.center = (self.rect.center[0], self.rect.center[1]+10)
            self.surface.blit(ISPRITE, ISPRITE_RECT)