
from GiGaia.GiServer.Game.userstate import Userstate
from GiGaia.GiCore.Game.states import STATE_IDS as SIDS
from GiGaia.GiCore.Game.World.coords import tileref_to_tile, tile_to_pix, add_coord, TILE_SIZE_PIXELS

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
        self.movement_expire = 0

        self.h.subscribe("CS_MOVE", self.handle_move_packet)
        self.h.subscribe("CS_JUMP", self.handle_jump_packet)
        self.h.subscribe("CS_CROUCH", self.handle_crouch_packet)
        self.h.subscribe("CS_WSET", self.handle_wset)
        self.h.subscribe("CS_DESTROY", self.handle_destroy)

        self.h.subscribe("CS_CHAT_OUT", self.handle_chat)

    def setup(self):

        self.data = self.game.world.data.get_player(self)
        if not self.data.exists:
            self.create_player()

        self.entity = self.game.entity_manager.spawn(Person, self.data.position, {"name":self.name}, player=self)
        self.h.send("SC_PLAYER", {'eid':self.entity.eid})
        self.game.players[self.name] = self

        self.game.world.update_time_player(self)

        self.inv = PlayerInventory(self)

        self.inv.add_dict(self.data.inventory)

    def create_player(self):
        self.data.create(
            start_pos = (random.randint(-100,100),-16000)
        )

    def leave(self): # Called when player leaves

        self.entity.destroy()

    def handle_chat(self, chat):

        self.game.chat.handle_chat(self, chat)

    def send_msg(self, msg, user='SERVER'):

        self.h.send("SC_CHAT", {'content':str(msg), 'user':user})

    def play_sound(self, sound):

        self.h.send("SC_SOUND", {'sound':sound})

    def update_entities(self):

        self.visible_entities.clear()
        vis_range = self.game.config.entity_visibility_range
        chunk_pos = self.entity.chunk_pos
        self.game.entity_manager.look(self, (chunk_pos[0]-vis_range, chunk_pos[1]-vis_range), (chunk_pos[0]+vis_range, chunk_pos[1]+vis_range))

    def handle_movement(self):

        #self.entity.position[0] += self.movement[0] * self.game.dt
        #self.entity.position[1] += self.movement[1] * self.game.dt
        self.entity.move(self.movement)
        if self.game.ticks > self.movement_expire:
            self.movement = 0

    def handle_move_packet(self, mp):
        self.movement_expire = self.game.ticks+mp.expire
        self.movement = math.copysign(1, mp.x)#max(self.movement[0], mp.x, key=abs)

    def handle_jump_packet(self, jp):

        self.entity.jump()

    def handle_crouch_packet(self, cp):

        if cp.crouching:
            self.entity.crouch()
        else:
            self.entity.stop_crouch()

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


    def handle_destroy(self, ds): # Tile destruction should be handled elsewhere
        
        dest_tile_id = self.game.world.get_chunk(ds.chunk).get(ds.tileref.x,ds.tileref.y,ds.tileref.z)
        if not dest_tile_id:
            return
        
        if dest_tile_id in self.game.assets.tiles: # To handle missing tile (eg. removed tile in dev)
            dest_tile = self.game.assets.tiles[dest_tile_id].name
            dest_pos = add_coord(tile_to_pix(tileref_to_tile((ds.chunk, (ds.tileref.x, ds.tileref.y)))), TILE_SIZE_PIXELS//2)

            self.game.entity_manager.spawn("ItemEntity", dest_pos, props={"item":f"tile{dest_tile}"}).add_velocity(random.randint(-9000,9000), random.randint(-9000,9000))
        self.game.world.get_chunk(ds.chunk).set_at(ds.tileref.x, ds.tileref.y, ds.tileref.z, 0)

    def tick(self):

        self.update_entities()
        self.handle_movement()

        self.inv.update()

        self.update_world()
