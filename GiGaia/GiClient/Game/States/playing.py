
from GiGaia.GiClient.Game.state import State
from GiGaia.GiClient.Game.Interfaces.playing import Playing as PlayingUI

from GiGaia.GiCore.Game.states import STATE_IDS as SIDS
from GiGaia.GiCore.Data.hashing import hash_pwd_nosalt

class Playing(State):

    def __init__(self, game):

        super().__init__(game, SIDS.PLAYING, PlayingUI)

        self.game_info = None

    def setup(self):

        pass

    def tick(self):

        pass