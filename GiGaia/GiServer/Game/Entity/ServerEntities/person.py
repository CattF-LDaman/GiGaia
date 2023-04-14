
from .entity import Entity
from GiGaia.GiCore.Game.Entities import Person as PersonBase

class Person(Entity, PersonBase):

    def __init__(self, entity_manager, eid, position, props, player):
        
        super().__init__(entity_manager, eid, position, props)

        self.player = player # Userstates.playing class

        self.em.game.log(f"{self.player.user.name} spawned at {self.position}")

    def tick(self):

        pass