
import pygame

class UIManager:

    def __init__(self, client):

        self.client = client

        self.assets = client.assets.assets
        self.window = client.window
        self.ui_layer = pygame.Surface(self.window.get_size())
        self.ui_layer.fill(self.assets.data.ui.colorkey)
        self.ui_layer.set_colorkey(self.assets.data.ui.colorkey)

        self.dimensions = self.ui_layer.get_size()

        self.widgets = [[] for _ in range(33)]

        self.capturing_input = []
        self.bp_press_start = 0
        self.bp_last = 0
        self.bp_delay = 400
        self.bp_replay_delay = 40

        self.rmb_clicks = []
        self.lmb_clicks = []
        self.scrolls_up = []
        self.scrolls_down = []

        self.resized = False

        self.cur_tick = 0
        self.update_frequency = self.assets.data.ui.update_freq
        self._prev_update = -100
        self.redraws = 0

    @property
    def has_head(self):
        for l in self.widgets:
            for w in l:
                if w.head_ui:
                    return True
        return False
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                self.rmb_clicks.append(event.pos)
            elif event.button == 1:
                self.lmb_clicks.append(event.pos)
            elif event.button == 4:
                self.scrolls_up.append(event.pos)
            elif event.button == 5:
                self.scrolls_down.append(event.pos)
        elif event.type == pygame.TEXTINPUT:
            for w in self.capturing_input:
                w.text_input += event.text
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.bp_press_start = self.bp_last = self.cur_tick
                for w in self.capturing_input:
                    w.text_input = w.text_input[:-1]
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                for w in self.capturing_input:
                    w.text_input += "\n"

    def capture_input(self, widget):
        if widget not in self.capturing_input:
            self.capturing_input.append(widget)

    def stop_capturing_input(self, widget):
        self.capturing_input.remove(widget)

    def add_widget(self, widget, *args, **kwargs):

        # self.client.log(f"[UI] New '{widget.__name__}' widget.", 1)
        w = widget(self, *args, **kwargs)
        self.widgets[w.layer].append(w)
        return w

    def update(self, ticks):

        self.cur_tick = ticks
        if ticks - self._prev_update > self.update_frequency:

            self.redraws = 0
            self.resized = False
            if self.ui_layer.get_size() != self.window.get_size():
                self.ui_layer = pygame.Surface(self.window.get_size())
                self.ui_layer.set_colorkey(self.assets.data.ui.colorkey)
                self.dimensions = self.ui_layer.get_size()
                self.resized = True

            self.ui_layer.fill(self.assets.data.ui.colorkey)

            if self.cur_tick - self.bp_press_start > self.bp_delay and pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                if self.cur_tick - self.bp_last > self.bp_replay_delay:
                    self.bp_last = self.cur_tick
                    for w in self.capturing_input:
                        w.text_input = w.text_input[:-1]

            widget_blits = []
            for layer in self.widgets:
                for widget in layer:
                    widget.update_master()
                    if (w_blit := widget.draw_master()):
                        widget_blits.append(w_blit)
            self.ui_layer.blits(widget_blits)

            self.rmb_clicks = []
            self.lmb_clicks = []
            self.scrolls_up = []
            self.scrolls_down = []

            self._prev_update = ticks

        self.window.blit(self.ui_layer, (0,0))