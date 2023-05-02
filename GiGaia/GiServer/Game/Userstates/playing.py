
from GiGaia.GiServer.Game.userstate import Userstate
from GiGaia.GiCore.Game.states import STATE_IDS as SIDS

from GiGaia.GiServer.Game.Entity.ServerEntities.person import Person
from GiGaia.GiServer.Game.Userstates.Playing.inventory import PlayerInventory

import random
import math

class Playing(Userstate):

    def __init__(self, user):
        super().__init__(user)

        self.name = user.name

        self.entity = None
        self.visible_entities = []

        self.served_chunks = []
        self.world_updates = {}

        self.movement = 0

        self.inv = PlayerInventory(self)
        self.inv.add_container("person")
        self.inv.add_item("person","jonko", 6, {"sleuren_left":69})

        self.h.subscribe("CS_MOVE", self.handle_move_packet)
        self.h.subscribe("CS_JUMP", self.handle_jump_packet)
        self.h.subscribe("CS_CROUCH", self.handle_crouch_packet)
        self.h.subscribe("CS_WSET", self.handle_wset)

    def setup(self):

        self.entity = self.game.entity_manager.spawn(Person, (random.randint(-100,100),-5000), {"name":self.name}, player=self)
        self.h.send("SC_PLAYER", {'eid':self.entity.eid})
        self.game.players[self.name] = self

        self.game.world.update_time_player(self)

    def leave(self): # Called when player leaves

        self.entity.destroy()

    def update_entities(self):

        self.visible_entities.clear()
        vis_range = self.game.config.entity_visibility_range
        chunk_pos = self.entity.chunk_pos
        self.game.entity_manager.look(self, (chunk_pos[0]-vis_range, chunk_pos[1]-vis_range), (chunk_pos[0]+vis_range, chunk_pos[1]+vis_range))

    def handle_movement(self):

        #self.entity.position[0] += self.movement[0] * self.game.dt
        #self.entity.position[1] += self.movement[1] * self.game.dt
        self.entity.move(self.movement)
        self.movement = 0

    def handle_move_packet(self, mp):
        self.movement = math.copysign(1, mp.x)#max(self.movement[0], mp.x, key=abs)

    def handle_jump_packet(self, jp):

        self.entity.jump()

    def handle_crouch_packet(self, cp):

        self.entity.crouch()

    def update_world(self):

        for chunk_pos, modifications in self.world_updates.items():
            if len(modifications) > self.game.world.config.chunk_tile_mod_max:
                self.h.send("SC_UPDATE_CHUNK", {"chunk":chunk_pos, "tiles":self.game.world.grab_chunk(chunk_pos).tiles})
            else:
                for mod in modifications:
                    self.h.send("SC_UPDATE_TILE", mod)
        self.world_updates.clear()

        self.served_chunks = self.game.world.serve(self)
        for c in self.served_chunks:
            self.game.world.grab_chunk(c).observers.append(self)

    def handle_wset(self, ws):

        self.game.world.get_chunk(ws.chunk).set_at(ws.tileref.x, ws.tileref.y, ws.tileref.z, ws.tile)

    def tick(self):

        self.update_entities()
        self.handle_movement()

        self.inv.update()

        self.update_world()
