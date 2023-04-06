
class State:

    def __init__(self, game, sid, interface):
        
        self.game = game
        self.client = game.client
        self.postman= self.p = game.postman

        self.inbox = {}

        self.ui = None
        if interface:
            self.ui = interface(self)

        self.sid = sid

    def setup_master(self):

        if self.ui:
            self.ui.create()

    def setup(self):

        pass

    def update(self):

        pass

    def tick(self):

        if self.ui:
            self.ui.update()

        self.update()