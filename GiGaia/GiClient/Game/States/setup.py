
from GiGaia.GiClient.Game.state import State
from GiGaia.GiClient.Game.Interfaces.setup import Setup as SetupUI

from GiGaia.GiCore.Game.states import STATE_IDS as SIDS
from GiGaia.GiCore.Data.hashing import hash_pwd_nosalt

class Setup(State):

    def __init__(self, game):

        super().__init__(game, SIDS.SETUP, SetupUI)

        self.game_info = None

        self.p.subscribe("SC_GAME_INFO", self.recv_game_info)

    def recv_game_info(self, gip):
        self.game_info = gip

    def submit(self, password):
        
        self.p.send("CS_LOGIN", {"password":hash_pwd_nosalt(password.encode("utf-8")+b'GiG', cycles=500)})

        OK = self.p.recv("SC_LOGIN_CONFIRM", 2)
        return OK

    def setup(self):

        self.game_info = self.p.recv("SC_GAME_INFO", 2)
        State.TICKRATE = self.game_info.tickrate
