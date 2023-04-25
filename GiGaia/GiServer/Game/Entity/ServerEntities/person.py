
from .entity import Entity
from .physical import Physical
from GiGaia.GiCore.Game.Entities import Person as PersonBase

class Person(Physical, PersonBase):

    PERSON_PHYSICS = {
        "mass": 95,
        "width": 30,
        "height": 60,
        "friction": 10,
        "air_friction": 10,
    }

    def __init__(self, entity_manager, eid, position, props, player):

        props.update(self.PERSON_PHYSICS)

        super().__init__(entity_manager, eid, position, props)

        self.player = player # Userstates.playing class

        self.em.game.log(f"{self.player.user.name} spawned at {self.position}")

    def move(self, movement):

        mx = movement
        speed = self.props["speed"]

        self.add_velocity(mx*speed if self.grounded else mx*speed)

    def jump(self):

        jump = self.props["jump_strength"]
        self.set_velocity(y=-jump if self.grounded else None)

    def crouch(self):

        self.ghost_platforms = True

    def tick(self):

        self.update_physics()

        self.ghost_platforms = False