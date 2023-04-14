
from GiGaia.GiServer.Game.userstate import Userstate
from GiGaia.GiCore.Game.states import STATE_IDS as SIDS

from GiGaia.GiServer.Game.Entity.ServerEntities.person import Person

class Playing(Userstate):

    def __init__(self, user):
        super().__init__(user)

        self.name = user.name

        self.entity = None
        self.visible_entities = []

    def setup(self):

        self.game.players[self.name] = self.user
        self.entity = self.game.entity_manager.spawn(Person, (0,0), {"name":self.name}, player=self)

    def update_entities(self):

        self.visible_entities.clear()
        vis_range = self.game.config.entity_visibility_range
        chunk_pos = self.entity.chunk_pos
        self.game.entity_manager.look(self, (chunk_pos[0]-vis_range, chunk_pos[1]-vis_range), (chunk_pos[0]+vis_range, chunk_pos[1]+vis_range))

    def tick(self):

        self.update_entities()