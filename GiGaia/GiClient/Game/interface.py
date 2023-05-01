

from GiGaia.GiClient.UI.Widgets.frame import Frame
class Interface:

    def __init__(self, state):

        self.state = state
        self.game = state.game
        self.ui_manager = self.uim = state.game.ui_manager

        self.ui = self.uim.add_widget(Frame, width=1.0, height=1.0, skip_event=True)

    def handle_event(self, event):

        pass

    def destroy(self):

        pass

    def create(self):

        pass

    def update(self):

        pass