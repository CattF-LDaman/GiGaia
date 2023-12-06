
from .physical import Physical

class Boink(Physical):

    ID = 1338
    NAME = "Boink"

    PROPERTIES = {
    }


    def __init__(self, eid, position=(0,0)):
        super().__init__(eid, position)
