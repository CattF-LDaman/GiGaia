
from .person import Person
from .bob import Bob
from .physical import Physical
from .firefly import Firefly

_ents = [Person, Bob, Physical, Firefly]

ENTITIES = {e.ID:e for e in _ents}