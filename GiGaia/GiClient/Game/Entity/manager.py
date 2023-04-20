
from .ClientEntities import ENTITIES

class EntityManager:

    def __init__(self, state):
        
        self.state = state
        self.scene = state.scene
        self.p = state.p
        self.game = state.game
    
        self.entities = {}
        self.entity_types = {}

        self.p.hold_all("SC_ENTITY","SC_ENTITY_POS","SC_ENTITY_UPD_PROP","SC_ENTITY_DESTROY")

    def spawn(self, entity, eid, position, props={}):

        ent = ENTITIES[entity]
        self.entities[eid] = ent(self, eid, position, props)

        if ent.ID not in self.entity_types:
            self.entity_types[ent.ID] = []
        self.entity_types[ent.ID].append(eid)

    def handle_packets(self):
        
        for e in self.p.fetch("SC_ENTITY"):

            self.spawn(e.id, e.eid, e.position, e.props.__dict__)

        for ep in self.p.fetch("SC_ENTITY_POS"):

            if ep.eid in self.entities:
                self.entities[ep.eid].update_position(ep.position)

        for epr in self.p.fetch("SC_ENTITY_UPD_PROP"):

            if epr.eid in self.entities:
                self.entities[epr.eid].update_props(epr.props.__dict__)

        for dp in self.p.fetch("SC_ENTITY_DESTROY"):
            
            if dp.eid in self.entities:
                self.entities[dp.eid].destroy()

    def remove(self, eid):

        rem = self.entities.pop(eid)
        rem.exists = False
        if rem.ID in self.entity_types:
            if eid in self.entity_types[rem.ID]:
                self.entity_types[rem.ID].remove(eid)

    def update(self):

        self.handle_packets()

        for e in self.entities.values():

            e.draw(self.game.screen)