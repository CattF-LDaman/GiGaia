
import pygame
import time

class Widget:

    def __init__(self, ui_manager, position=(0,0), layer=0, width=1, height=1, max_width=None, max_height=None, min_width=None, min_height=None, anchor="topleft", relative_to=None, relative_anchor=None, child_of=None, always_redraw=False, skip_draw=False, skip_event=False, head_ui=False, vanish_after=0, **kwargs):

        self.ui_manager = self.uim = ui_manager
        self.client = ui_manager.client

        self.head_ui = head_ui

        if head_ui:
            for l in self.ui_manager.widgets:
                for w in l:
                    if w.head_ui:
                        w.delete()

        self.position = list(position)
        self.layer = layer

        self._size = (width, height)
        self._max_size = (max_width, max_height)
        self._min_size = (min_width, min_height)
        self.anchor = anchor
        self.relative_to = self.parent = relative_to
        self.relative_anchor = relative_anchor

        if self.relative_to:
            self.relative_to.children.append(self)

        if child_of:
            child_of.children.append(self)

        self.surface = pygame.Surface(self.size)
        self.surface.set_colorkey(self.uim.assets.data.ui.colorkey)
        self.surface.fill(self.uim.assets.data.ui.colorkey)

        self.updated = True
        self.always_redraw = always_redraw
        self.skip_draw = skip_draw
        self.skip_event = skip_event
        self.hidden = False
        self.disable_updates = False
        self.resized = False

        self.vanish_after = vanish_after
        self.birth = self.uim.cur_tick

        self.hovered = False
        self.hovered_once = False
        self.unhovered = False
        self.clicked = False
        self.unclicked = False
        self.r_clicked = False
        self.scrolled_up = False
        self.scrolled_down = False
        self.held = False
        self.hold_start = None

        self.children = []

        self.deleted = False

        self.text_input = ""

    def handle_resize(self):
        pass

    def handle_delete(self):
        pass

    def draw(self):
        pass

    def update(self):
        pass

    def start_input(self):
        if self not in self.uim.capturing_input:
            self.uim.capture_input(self)

    def stop_input(self):
        if self in self.uim.capturing_input:
            self.uim.stop_capturing_input(self)

    def resize(self, w=None, h=None):
        nz = list(self._size)
        if w: nz[0] = w
        if h: nz[1] = h
        self._size = tuple(nz)
        self.resized = True

    def hide(self):
        self.hidden = True
        for child in self.children:
            child.hide()

    def reveal(self):
        self.hidden = False
        for child in self.children:
            child.reveal()

    @property
    def age(self):
        return self.uim.cur_tick - self.birth

    @property
    def capturing(self):
        return self in self.uim.capturing_input

    @property
    def height(self):
        return self.size[1]

    @property
    def width(self):
        return self.size[0]

    @property
    def size(self):
        size = []
        if type(self._size[0]) == float:
            if self.relative_to:
                size.append(int(self.relative_to.size[0]*self._size[0]))
            else:
                size.append(int(self.ui_manager.dimensions[0]*self._size[0]))
        else:
            size.append(self._size[0])

        if type(self._size[1]) == float:
            if self.relative_to:
                size.append(int(self.relative_to.size[1]*self._size[1]))
            else:
                size.append(int(self.ui_manager.dimensions[1]*self._size[1]))
        else:
            size.append(self._size[1])

        if self._max_size[0]:
            size[0] = min(self._max_size[0], size[0])
        if self._max_size[1]:
            size[1] = min(self._max_size[1], size[1])

        if self._min_size[0]:
            size[0] = max(self._min_size[0], size[0])
        if self._min_size[1]:
            size[1] = max(self._min_size[1], size[1])

        return size

    @property
    def abs_position(self):
        pos = []
        if self.relative_to:
            rel_pos = getattr(self.relative_to.widget_rect, self.relative_anchor) if self.relative_anchor else self.relative_to.abs_position
        if type(self.position[0]) == float:
            if self.relative_to:
                pos.append(rel_pos[0]+(self.relative_to.size[0]*self.position[0]))
            else:
                pos.append(self.ui_manager.dimensions[0]*self.position[0])
        elif self.relative_to:
            pos.append(rel_pos[0]+self.position[0])
        else:
            pos.append(self.position[0])

        if type(self.position[1]) == float:
            if self.relative_to:
                pos.append(rel_pos[1]+(self.relative_to.size[1]*self.position[1]))
            else:
                pos.append(self.ui_manager.dimensions[1]*self.position[1])
        elif self.relative_to:
            pos.append(rel_pos[1]+self.position[1])
        else:
            pos.append(self.position[1])

        return pos

    @property
    def widget_rect(self):  # Rectangle on window
        return self.surface.get_rect(**{self.anchor:self.abs_position})

    @property
    def rect(self):  # Rectangle with topleft as 0,0
        return self.surface.get_rect()

    def delete(self):
        if not self.deleted:
            self.handle_delete()
            self.stop_input()
            for child in self.children:
                child.delete()
            self.ui_manager.widgets[self.layer].remove(self)
            self.deleted = True

    def draw_master(self):
        if self.skip_draw or self.hidden:
            return

        if self.updated or self.always_redraw:
            self.draw()
            self.uim.redraws += 1
            self.updated = False

        return (self.surface, self.widget_rect)
        self.ui_manager.ui_layer.blit(self.surface, self.widget_rect)

    def update_master(self):

        if self.uim.resized or self.resized:
            self.surface = pygame.Surface(self.size)
            self.surface.set_colorkey(self.uim.assets.data.ui.colorkey)
            self.handle_resize()
            self.updated = True
            self.resized = False

        if not self.skip_event:

            was_h = self.hovered
            self.hovered_once = False
            self.hovered = False
            self.unhovered = False
            self.clicked = False
            self.r_clicked = False
            self.scrolled_up = False
            self.scrolled_down = False
            self.unclicked = False

            if self.age != 0 and not self.hidden:
                if not pygame.mouse.get_pressed()[0]:
                    self.held = False

                if self.widget_rect.collidepoint(pygame.mouse.get_pos()):
                    if not was_h:
                        self.hovered_once = True
                    else:
                        self.hovered_once = False
                    self.hovered = True
                elif was_h:
                    self.unhovered = True

                for r_cl in self.ui_manager.rmb_clicks:
                    if self.widget_rect.collidepoint(r_cl):
                        self.r_clicked = True

                for l_cl in self.ui_manager.lmb_clicks:
                    if self.widget_rect.collidepoint(l_cl):
                        self.clicked = True
                        if not self.held:
                            self.hold_start = l_cl
                        self.held = True
                    else:
                        self.unclicked = True

                for u_sc in self.ui_manager.scrolls_up:
                    if self.widget_rect.collidepoint(u_sc):
                        self.scrolled_up = True

                for d_sc in self.ui_manager.scrolls_down:
                    if self.widget_rect.collidepoint(d_sc):
                        self.scrolled_down = True

        if not self.disable_updates:
            self.update()

        if self.vanish_after and self.age > self.vanish_after:
            self.delete()