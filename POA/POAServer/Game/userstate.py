
from POA.POACore.threading import threaded_daemon

class Userstate:

    def __init__(self, user):

        self.user = user
        self.handle = self.h = user.handle
        self.game = user.game
        self.realm = user.game.realm

        self.ready = False
    
    def setup(self):

        pass

    def tick(self):

        pass

    @threaded_daemon
    def _setup(self):

        self.setup()
        self.ready = True
