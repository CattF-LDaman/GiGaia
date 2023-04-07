
from GiGaia.GiClient.Game.state import State
from GiGaia.GiClient.Game.Interfaces.setup import Setup as SetupUI

from GiGaia.GiCore.Game.states import STATE_IDS as SIDS
from GiGaia.GiCore.Data.hashing import hash_pwd_nosalt

class Setup(State):

    def __init__(self, game):

        super().__init__(game, SIDS.SETUP, SetupUI)

    def submit(self, user, password):

        self.p.send("CS_LOGIN", {"user":user, "password":hash_pwd_nosalt(password.encode("utf-8")+b'GiG', cycles=500)})

        OK = self.p.recv("SC_NATION_OK", 2)
        return OK

    def setup(self):

        pass