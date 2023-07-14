
from .person import Person
from .bob import Bob
from .firefly import Firefly

_ents = [Person, Bob, Firefly]

ENTITIES = {ent.ID:ent for ent in _ents}
ENTITIES_NAME = {ent.NAME:ent for ent in _ents}