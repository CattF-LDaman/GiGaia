
from GiGaia.GiServer.Data.userdata import UserData
from .Userstates import STATES
from GiGaia.GiCore.Game.states import STATE_IDS as SIDS

class User:

    def __init__(self, game, handle):
        
        self.game = game
        self.handle = handle

        self.name = handle.username
        self.left = False

        self.data = UserData(self.game.dirs["users"], self.name)

        self.state = None
    
    def disconnect(self, reason="No reason specified."):

        self.game.log(f"User '{self.name}' disconnected by server: {reason}")
        self.handle.close()

    def switch_state(self, sid):

        self.state = STATES[sid](self)
        self.handle.send("SC_LOAD_STATE", {"sid":sid})
        self.state._setup()

    def setup(self):

        self.switch_state(SIDS.SETUP)