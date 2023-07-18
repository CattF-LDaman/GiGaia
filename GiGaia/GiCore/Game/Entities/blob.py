
from .physical import Physical

class Blob(Physical):

    ID = 1337
    NAME = "Blob"

    PROPERTIES = {
    }


    def __init__(self, eid, position=(0,0)):
        super().__init__(eid, position)
