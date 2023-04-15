
from .person import Person
from .bob import Bob

_ents = [Person, Bob]

ENTITIES = {ent.ID:ent for ent in _ents}
ENTITIES_NAME = {ent.NAME:ent for ent in _ents}