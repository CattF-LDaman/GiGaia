
from .entity import Entity
from .physical import Physical
from GiGaia.GiCore.Game.Entities import Person as PersonBase

class Person(Physical, PersonBase):

    PERSON_PHYSICS = {
        "mass": 115,
        "width": 30,
        "height": 60-4,
        "friction": 10,
        "air_friction": 9,
    }

    def __init__(self, entity_manager, eid, position, props, player):

        props.update(self.PERSON_PHYSICS)

        super().__init__(entity_manager, eid, position, props)

        self.player = player # Userstates.playing class

        self.step_up = True

        self.em.game.log(f"{self.player.user.name} spawned at {self.position}")

    def move(self, movement):

        mx = movement
        speed = self.props["speed"]

        self.add_velocity(mx*speed if not self.props["flying"] else mx*self.props["flight_speed"])

    def jump(self):

        if not self.props["flying"]:
            self.set_velocity(y=-self.props["jump_strength"] if self.grounded else None)
        else:
            self.add_velocity(y=-self.props["flight_speed"])

    def crouch(self):
        if self.props["flying"]:
            self.add_velocity(y=self.props["flight_speed"])
        self.ghost_platforms = True

    def stop_crouch(self):

        self.ghost_platforms = False

    def toggle_flight(self):

        if not self.props["flying"]:
            self.change("flying", True)
            self.change("has_gravity", False)
            return True
        else:
            self.change("has_gravity", True)
            self.change("flying", False)
            return False

    def tick(self):
        
        self.get_seen(self.player)
        self.update_physics()
