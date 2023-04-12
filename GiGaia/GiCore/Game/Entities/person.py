
from .entity import Entity

class Person(Entity):

    ID = 1
    NAME = "Person"

    def __init__(self, eid, position=(0,0)):
        super().__init__(eid, position)

    