
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

    def destroy_master(self):

        if self.ui:
            self.ui.destroy()
        self.destroy()

    def setup_master(self):

        self.p.send("A_WAITING")
        self.setup()
        if self.ui:
            self.ui.create()

    def handle_event_master(self, event):

        if self.ui:
            self.ui.handle_event(event)
        self.handle_event(event)

    def destroy(self): # Called before switching to another state

        pass

    def setup(self): # Called before UI creation

        pass

    def update(self): # Called every tick right after UI update

        pass

    def handle_event(self, event):

        pass

    def tick(self):

        if self.ui:
            self.ui.update()

        self.update()