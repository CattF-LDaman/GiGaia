
from .person import Person
from .bob import Bob
from .bitch import Bitch

_ents = [Person, Bob, Bitch]

ENTITIES = {ent.ID:ent for ent in _ents}
ENTITIES_NAME = {ent.NAME:ent for ent in _ents}