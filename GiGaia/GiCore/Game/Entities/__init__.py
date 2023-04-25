
from .person import Person
from .bob import Bob
from .physical import Physical

_ents = [Person, Bob, Physical]

ENTITIES = {e.ID:e for e in _ents}