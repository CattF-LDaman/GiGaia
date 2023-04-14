
from .person import Person
from .bob import Bob

_ents = [Person, Bob]

ENTITIES = {e.ID:e for e in _ents}