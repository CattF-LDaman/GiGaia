
from GiGaia.GiClient.Game.state import State
from GiGaia.GiClient.Game.Interfaces.playing import Playing as PlayingUI

from GiGaia.GiCore.Game.states import STATE_IDS as SIDS

class Playing(State):

    def __init__(self, game):

        super().__init__(game, SIDS.PLAYING, PlayingUI)

        self.game_info = None

        self.p.hold("SC_ENTITY")
        self.p.hold("SC_ENTITY_POS")
        self.p.hold("SC_ENTITY_UPD_PROP")

    def setup(self):

        pass

    def tick(self):
        
        self.p.fetch("SC_ENTITY")
        self.p.fetch("SC_ENTITY_POS")
        self.p.fetch("SC_ENTITY_UPD_PROP")
