
from .person import Person
from .bob import Bob
from .physical import Physical
from .firefly import Firefly
from .blob import Blob

_ents = [Person, Bob, Physical, Firefly, Blob]

ENTITIES = {e.ID:e for e in _ents}