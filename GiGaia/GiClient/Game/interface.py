
class Interface:

    def __init__(self, state):

        self.state = state
        self.game = state.game
        self.ui_manager = self.uim = state.game.ui_manager

    def destroy(self):

        pass

    def create(self):

        pass

    def update(self):

        pass