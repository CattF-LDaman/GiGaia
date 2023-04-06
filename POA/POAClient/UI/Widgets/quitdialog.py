
from POA.POAClient.UI.widget import Widget

import pygame

class QuitDialog(Widget):

    def __init__(self, ui_manager):

        super().__init__(ui_manager, position=[0.5, 0.5], layer=26, width=0.5, height=200, anchor="center", always_redraw=False, head_ui=True)
        self.y_button = self.uim.add_widget(QuitDialogButtonYes, self)
        self.n_button = self.uim.add_widget(QuitDialogButtonNo, self)

        self.inner_rect = pygame.Rect(0,0,0,0)
        self.inner_rect.width = self.size[0]-10
        self.inner_rect.height = self.size[1]-10
        self.inner_rect.center = self.rect.center

    def handle_resize(self):
        self.inner_rect = pygame.Rect(0,0,0,0)
        self.inner_rect.width = self.size[0]-10
        self.inner_rect.height = self.size[1]-10
        self.inner_rect.center = self.rect.center

    def update(self):

        pass

    def draw(self):

        self.surface.fill(self.uim.assets.data.ui.color_A)
        pygame.draw.rect(self.surface, self.uim.assets.data.ui.color_B, self.inner_rect, width=4)
        self.uim.assets.fonts["basic"].render(self.surface, self.rect.midtop+pygame.Vector2(0,40), "Are you sure?", blit_anchor_center=True, scale=3)

class QuitDialogButtonNo(Widget):

    def __init__(self, ui_manager, diag):

        super().__init__(ui_manager, position=[-130, 0.2], layer=27, width=100, height=50, anchor="center", relative_to=diag, always_redraw=False)
        self.diag = diag

    def update(self):

        if self.hovered_once:
            self.uim.assets.sounds["hover"].play()

        self.updated = (self.hovered_once or self.unhovered) or self.updated

        if self.clicked:
            self.uim.assets.sounds["click"].play()
            self.diag.delete()

    def draw(self):

        if not self.hovered:
            self.surface.fill((20,20,20))
        else:
            self.surface.fill((40,40,40))
        self.uim.assets.fonts["basic"].render(self.surface, self.rect.center+pygame.Vector2(0,5), "No", blit_anchor_center=True, scale=2)

class QuitDialogButtonYes(Widget):

    def __init__(self, ui_manager, diag):

        super().__init__(ui_manager, position=[130, 0.2], layer=27, width=100, height=50, anchor="center", relative_to=diag, always_redraw=False)
        self.diag = diag

    def update(self):

        if self.hovered_once:
            self.uim.assets.sounds["hover"].play()

        self.updated = (self.hovered_once or self.unhovered) or self.updated

        if self.clicked:
            self.uim.assets.sounds["click"].play()
            self.uim.client.game.close()

    def draw(self):

        if not self.hovered:
            self.surface.fill((20,20,20))
        else:
            self.surface.fill((40,40,40))
        self.uim.assets.fonts["basic"].render(self.surface, self.rect.center+pygame.Vector2(0,5), "Yes", blit_anchor_center=True, scale=2)
