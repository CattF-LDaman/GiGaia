
from POA.POAClient.Game.state import State
from POA.POAClient.Game.Interfaces.setup import Setup as SetupUI

from POA.POACore.Game.states import STATE_IDS as SIDS

class Setup(State):

    def __init__(self, game):

        super().__init__(game, SIDS.SETUP, SetupUI)

    def submit(self, name, motto):

        self.p.send("CS_CREATE_NATION", {"name":name, "motto":motto})

        OK = self.p.recv("SC_NATION_OK", 2)
        return OK

    def setup(self):

        pass