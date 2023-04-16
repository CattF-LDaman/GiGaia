
from GiGaia.GiServer.Game.userstate import Userstate
from GiGaia.GiCore.Game.states import STATE_IDS as SIDS

from GiGaia.GiServer.Game.Entity.ServerEntities.person import Person

import random

class Playing(Userstate):

    def __init__(self, user):
        super().__init__(user)

        self.name = user.name

        self.entity = None
        self.visible_entities = []

        self.movement = [0, 0]

        self.h.subscribe("CS_MOVE", self.handle_move_packet)

    def setup(self):

        self.game.players[self.name] = self
        self.entity = self.game.entity_manager.spawn(Person, (random.randint(-100,100),random.randint(-100,100)), {"name":self.name}, player=self)
        self.h.send("SC_PLAYER", {'eid':self.entity.eid})

    def leave(self): # Called when player leaves

        self.entity.destroy()

    def update_entities(self):

        self.visible_entities.clear()
        vis_range = self.game.config.entity_visibility_range
        chunk_pos = self.entity.chunk_pos
        self.game.entity_manager.look(self, (chunk_pos[0]-vis_range, chunk_pos[1]-vis_range), (chunk_pos[0]+vis_range, chunk_pos[1]+vis_range))

    def handle_movement(self):

        self.entity.position[0] += self.movement[0] * self.game.dt
        self.entity.position[1] += self.movement[1] * self.game.dt
        self.movement = [0, 0]

    def handle_move_packet(self, mp):
        self.movement[0] = max(self.movement[0], mp.x, key=abs)
        self.movement[1] = max(self.movement[1], mp.y, key=abs)

    def tick(self):

        self.update_entities()
        self.handle_movement()