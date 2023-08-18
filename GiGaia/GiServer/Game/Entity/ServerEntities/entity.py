
from GiGaia.GiCore.Game.Entities.entity import Entity as EntityBase
from GiGaia.GiCore.Game.World.coords import floor_coord

class Entity(EntityBase):

    def __init__(self, entity_manager, eid, position, props):
        super().__init__(eid, position)

        self.em = self.entity_manager = entity_manager
        self.game = self.em.game

        self.seen_by = []
        self.changes = {}

        self.prev_pos = None

        self.destroyed = False

        self.set_properties(props)

    def tick(self):

        pass

    def destroy(self):

        if self.destroyed:
            return
        
        self.em.remove(self.eid)
        self._destroy()
        
        self.destroyed = True

    def _destroy(self):

        for player in self.seen_by:
            player.h.send("SC_ENTITY_DESTROY", {"eid":self.eid})

    def change(self, prop, val):

        if prop not in self.props:
            raise ValueError(f"Property '{prop}' doesn't exist.")

        if self.props[prop] == val:
            return

        self.props[prop] = val
        self.changes[prop] = val

    def _update_properties(self):
        if self.changes:
            for player in self.seen_by:
                player.h.send("SC_ENTITY_UPD_PROP", {"eid":self.eid, "props":(list(prop for prop in self.PROPERTIES if prop[0] in self.changes),self.changes.copy())})
            self.changes.clear()

    def get_seen(self, player):
        player.visible_entities.append(self)
        if player not in self.seen_by:
            self.seen_by.append(player)
            self.em.traffic.send(player.name, "SC_ENTITY", {"eid":self.eid, "id":self.ID, "position":self.position, "props":(self.PROPERTIES.keys(), self.props)})

    def _update_position(self):
        #self.position[0], self.position[1] = int(self.position[0]), int(self.position[1])
        if floor_coord(self.position) != self.prev_pos:
            for player in self.seen_by:
                player.h.send("SC_ENTITY_POS", {"eid":self.eid, "position":self.position}, unique_val="eid", important=player.entity==self)
            self.prev_pos = floor_coord(self.position)

    def update(self):

        if self.chunk_pos not in self.em.map:
            self.em.map[self.chunk_pos] = []
        self.em.map[self.chunk_pos].append(self)

        self.tick()
        self._update_position()
        self._update_properties()

        for player in (p for p in self.seen_by if self not in p.visible_entities or p.user.left):
            self.seen_by.remove(player)
            player.h.send("SC_ENTITY_DESTROY", {"eid":self.eid})
