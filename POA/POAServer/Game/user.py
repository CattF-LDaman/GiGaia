
from .Userstates import STATES
from POA.POACore.Game.states import STATE_IDS as SIDS

class User:

    def __init__(self, game, handle):
        
        self.game = game
        self.handle = handle

        self.name = handle.username

        self.state = None
    
    def switch_state(self, sid):

        self.state = STATES[sid](self)
        self.handle.send("SC_LOAD_STATE", {"sid":sid})
        self.state._setup()

    def setup(self):

        self.switch_state(SIDS.SETUP)