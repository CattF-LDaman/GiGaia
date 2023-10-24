
from GiGaia.GiCore.threading import threaded_daemon

import time

class Userstate:

    def __init__(self, user):

        self.user = user
        self.handle = self.h = user.handle
        self.game = user.game
        self.log = user.game.log

        self.ready = False
    
    def setup(self):

        pass

    def tick(self):

        pass

    @threaded_daemon
    def _setup(self):

        self.h.recv("A_WAITING")
        time.sleep(0.5)
        self.setup()
        self.ready = True
