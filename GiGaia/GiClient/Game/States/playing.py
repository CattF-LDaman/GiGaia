
from GiGaia.GiClient.Game.state import State
from GiGaia.GiClient.Game.Interfaces.playing import Playing as PlayingUI

from GiGaia.GiClient.Game.Entity.manager import EntityManager
from GiGaia.GiClient.Game.scene import Scene

from GiGaia.GiCore.Game.states import STATE_IDS as SIDS

class Playing(State):

    def __init__(self, game):

        super().__init__(game, SIDS.PLAYING, PlayingUI)

        self.scene = Scene(game.screen)
        self.entity_manager = EntityManager(self)

    @property
    def player(self):
        if self.player_eid and self.player_eid in self.entity_manager.entities:
            return self.entity_manager.entities[self.player_eid]

    def setup(self):

        self.player_eid = self.p.recv("SC_PLAYER").eid

    def tick(self):
        
        self.entity_manager.update()
        
