
from .person import Person
from .bob import Bob
from .physical import Physical
from .bitch import Bitch

_ents = [Person, Bob, Physical, Bitch]

ENTITIES = {e.ID:e for e in _ents}