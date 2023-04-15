
from .ServerEntities import ENTITIES_NAME, ENTITIES

from GiGaia.GiCore.Game.World.coords import coord_range

class EntityManager:

    def __init__(self, game):
        
        self.game = game
        self.traffic = self.t = game.traffic

        self.entities = {}
        self._cur_eid = 0 # Entity Instance ID

        self.map = {}

    def _get_eid(self):

        self._cur_eid += 1
        return self._cur_eid
    
    def spawn(self, entity, position, props={}, *args, **kwargs):
        
        match entity:
            case int(id):
                entity = ENTITIES[id]
            case str(name):
                entity = ENTITIES_NAME[name]

        eid = self._get_eid()
        self.entities[eid] = e = entity(self, eid, position, props, *args, **kwargs)
        return e
    
    def remove(self, eid):

        self.entities.pop(eid)._destroy()

    def look(self, player, A, B):

        chunks = coord_range(A, B)
        for chunk in chunks:
            if chunk in self.map:
                seen = self.map[chunk]
                for ent in seen:
                    ent.get_seen(player)

    def update(self):

        self.map = {}

        for entity in self.entities.values():

            entity.update()